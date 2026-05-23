import logging
import warnings
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import joblib

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


class AIAgentEnsembleRegressor(BaseRegressionModel):
    """
    AI Agent 集成回归模型
    
    特点:
    1. 多模型集成 (RandomForest + GradientBoosting + LinearRegression)
    2. 自适应权重调整
    3. 市场状态识别
    4. 动态特征选择
    5. 风险评估集成
    """

    def __init__(self, dk: FreqaiDataKitchen, **kwargs):
        super().__init__(dk=dk, **kwargs)
        # 基础模型
        self.models = {
            'rf': RandomForestRegressor(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            ),
            'gb': GradientBoostingRegressor(
                n_estimators=150,
                max_depth=6,
                learning_rate=0.1,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'lr': LinearRegression()
        }
        
        # 模型权重 (动态调整)
        self.model_weights = {
            'rf': 0.4,
            'gb': 0.4, 
            'lr': 0.2
        }
        
        # 市场状态分类器
        self.market_state_classifier = None
        
        # 特征重要性
        self.feature_importance = {}
        
        # 模型性能记录
        self.model_performance = {
            'rf': {'mse': [], 'r2': []},
            'gb': {'mse': [], 'r2': []},
            'lr': {'mse': [], 'r2': []}
        }

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """训练模型"""
        
        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]
        
        logger.info(f"Training AI Agent Ensemble with {X.shape[0]} samples, {X.shape[1]} features")
        
        # 特征选择和预处理
        X_processed, selected_features = self._preprocess_features(X, y, dk)
        self.selected_features = selected_features
        
        # 市场状态识别
        market_states = self._identify_market_states(X_processed, y)
        
        # 训练各个基础模型
        trained_models = {}
        model_scores = {}
        
        for name, model in self.models.items():
            logger.info(f"Training {name} model...")
            
            try:
                # 训练模型
                model.fit(X_processed, y.values.ravel())
                trained_models[name] = model
                
                # 交叉验证评估
                cv_scores = cross_val_score(model, X_processed, y.values.ravel(), 
                                          cv=5, scoring='neg_mean_squared_error')
                mse_score = -cv_scores.mean()
                r2_scores = cross_val_score(model, X_processed, y.values.ravel(), 
                                          cv=5, scoring='r2')
                r2_score = r2_scores.mean()
                
                model_scores[name] = {
                    'mse': mse_score,
                    'r2': r2_score,
                    'cv_std': cv_scores.std()
                }
                
                # 记录性能
                self.model_performance[name]['mse'].append(mse_score)
                self.model_performance[name]['r2'].append(r2_score)
                
                logger.info(f"{name} - MSE: {mse_score:.6f}, R2: {r2_score:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {name}: {e}")
                continue
        
        # 动态调整模型权重
        self._update_model_weights(model_scores)
        
        # 提取特征重要性
        self._extract_feature_importance(trained_models, X_processed.columns)
        
        # 训练市场状态分类器
        self._train_market_state_classifier(X_processed, market_states)
        
        # 保存训练好的模型
        self.trained_models = trained_models
        
        logger.info(f"Model weights: {self.model_weights}")
        logger.info("AI Agent Ensemble training completed")
        
        return self

    def predict(self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs) -> Tuple[DataFrame, DataFrame]:
        """预测"""
        
        # 预处理特征
        X = unfiltered_df[self.selected_features] if hasattr(self, 'selected_features') else unfiltered_df
        
        # 检测当前市场状态
        current_market_state = self._predict_market_state(X)
        
        # 基于市场状态调整权重
        adjusted_weights = self._adjust_weights_for_market_state(current_market_state)
        
        # 各模型预测
        predictions = {}
        prediction_confidence = {}
        
        for name, model in self.trained_models.items():
            try:
                pred = model.predict(X)
                predictions[name] = pred
                
                # 计算预测置信度
                if hasattr(model, 'predict_proba'):
                    # 对于支持概率预测的模型
                    confidence = np.max(model.predict_proba(X), axis=1)
                elif hasattr(model, 'score'):
                    # 基于训练得分估算置信度
                    confidence = np.full(len(pred), 0.8)  
                else:
                    confidence = np.full(len(pred), 0.7)
                    
                prediction_confidence[name] = confidence
                
            except Exception as e:
                logger.error(f"Error predicting with {name}: {e}")
                predictions[name] = np.zeros(len(X))
                prediction_confidence[name] = np.zeros(len(X))
        
        # 集成预测
        ensemble_pred = np.zeros(len(X))
        ensemble_confidence = np.zeros(len(X))
        
        total_weight = sum(adjusted_weights.values())
        
        for name, pred in predictions.items():
            weight = adjusted_weights.get(name, 0) / total_weight
            ensemble_pred += weight * pred
            ensemble_confidence += weight * prediction_confidence[name]
        
        # 创建预测结果DataFrame
        pred_df = DataFrame(ensemble_pred, columns=dk.label_list, index=unfiltered_df.index)
        
        # 创建预测置信度DataFrame  
        confidence_df = DataFrame(ensemble_confidence, columns=['confidence'], index=unfiltered_df.index)
        
        # 添加市场状态信息
        pred_df['market_state'] = current_market_state
        pred_df['prediction_confidence'] = ensemble_confidence
        
        # 添加各模型的预测结果 (用于分析)
        for name, pred in predictions.items():
            pred_df[f'{name}_prediction'] = pred
        
        return pred_df, confidence_df

    def _preprocess_features(self, X: DataFrame, y: DataFrame, dk: FreqaiDataKitchen) -> Tuple[DataFrame, list]:
        """特征预处理和选择"""
        
        # 移除缺失值过多的特征
        missing_threshold = 0.1
        missing_ratios = X.isnull().sum() / len(X)
        valid_features = missing_ratios[missing_ratios <= missing_threshold].index.tolist()
        
        X_cleaned = X[valid_features].fillna(method='ffill').fillna(0)
        
        # 移除方差过小的特征
        feature_vars = X_cleaned.var()
        high_var_features = feature_vars[feature_vars > 1e-6].index.tolist()
        
        X_filtered = X_cleaned[high_var_features]
        
        # 相关性过滤 (移除与目标变量相关性过低的特征)
        if len(y) > 50:  # 确保有足够样本计算相关性
            correlations = X_filtered.corrwith(y.iloc[:, 0])
            corr_threshold = 0.01
            relevant_features = correlations[abs(correlations) > corr_threshold].index.tolist()
            X_final = X_filtered[relevant_features] if relevant_features else X_filtered
        else:
            X_final = X_filtered
        
        logger.info(f"Feature selection: {X.shape[1]} -> {X_final.shape[1]} features")
        
        return X_final, X_final.columns.tolist()

    def _identify_market_states(self, X: DataFrame, y: DataFrame) -> np.ndarray:
        """识别市场状态"""
        
        if len(y) < 50:
            return np.zeros(len(y))
        
        # 基于价格波动性和趋势识别市场状态
        # 0: 震荡市场, 1: 上升趋势, 2: 下降趋势, 3: 高波动市场
        
        returns = y.values.ravel()
        volatility = pd.Series(returns).rolling(window=20, min_periods=5).std()
        trend = pd.Series(returns).rolling(window=20, min_periods=5).mean()
        
        states = np.zeros(len(returns))
        
        for i in range(len(returns)):
            vol = volatility.iloc[i] if i < len(volatility) else volatility.iloc[-1]
            tr = trend.iloc[i] if i < len(trend) else trend.iloc[-1]
            
            if pd.isna(vol) or pd.isna(tr):
                states[i] = 0
                continue
                
            # 高波动市场
            if vol > np.nanpercentile(volatility.dropna(), 80):
                states[i] = 3
            # 上升趋势
            elif tr > np.nanpercentile(trend.dropna(), 60):
                states[i] = 1
            # 下降趋势  
            elif tr < np.nanpercentile(trend.dropna(), 40):
                states[i] = 2
            # 震荡市场
            else:
                states[i] = 0
        
        return states

    def _train_market_state_classifier(self, X: DataFrame, states: np.ndarray):
        """训练市场状态分类器"""
        
        try:
            from sklearn.ensemble import RandomForestClassifier
            
            self.market_state_classifier = RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                random_state=42
            )
            
            # 选择与市场状态最相关的特征
            if len(X) > 50:
                state_features = []
                for col in X.columns:
                    try:
                        corr = np.corrcoef(X[col].fillna(0), states)[0, 1]
                        if not np.isnan(corr) and abs(corr) > 0.05:
                            state_features.append(col)
                    except:
                        continue
                
                if state_features:
                    X_state = X[state_features].fillna(0)
                    self.market_state_classifier.fit(X_state, states)
                    self.state_features = state_features
                    logger.info(f"Market state classifier trained with {len(state_features)} features")
                else:
                    self.market_state_classifier = None
            
        except Exception as e:
            logger.error(f"Error training market state classifier: {e}")
            self.market_state_classifier = None

    def _predict_market_state(self, X: DataFrame) -> np.ndarray:
        """预测当前市场状态"""
        
        if self.market_state_classifier is None or not hasattr(self, 'state_features'):
            return np.zeros(len(X))
        
        try:
            X_state = X[self.state_features].fillna(0)
            states = self.market_state_classifier.predict(X_state)
            return states
        except Exception as e:
            logger.error(f"Error predicting market state: {e}")
            return np.zeros(len(X))

    def _update_model_weights(self, model_scores: Dict):
        """动态更新模型权重"""
        
        if not model_scores:
            return
        
        # 基于R2分数更新权重 (R2越高权重越大)
        r2_scores = {name: scores.get('r2', 0) for name, scores in model_scores.items()}
        
        # 确保所有R2分数为正数
        min_r2 = min(r2_scores.values())
        if min_r2 < 0:
            r2_scores = {name: score - min_r2 + 0.1 for name, score in r2_scores.items()}
        
        # 计算权重 (基于R2分数的softmax)
        total_score = sum(r2_scores.values())
        if total_score > 0:
            new_weights = {name: score / total_score for name, score in r2_scores.items()}
            
            # 平滑权重更新 (避免剧烈变化)
            alpha = 0.3  # 学习率
            for name in self.model_weights:
                if name in new_weights:
                    self.model_weights[name] = (
                        alpha * new_weights[name] + 
                        (1 - alpha) * self.model_weights[name]
                    )

    def _adjust_weights_for_market_state(self, market_states: np.ndarray) -> Dict:
        """根据市场状态调整权重"""
        
        adjusted_weights = self.model_weights.copy()
        
        if len(market_states) == 0:
            return adjusted_weights
        
        # 获取当前主导市场状态
        current_state = int(np.round(np.mean(market_states[-10:])))  # 最近10个预测的平均状态
        
        # 根据市场状态调整权重
        if current_state == 0:  # 震荡市场
            # 线性模型在震荡市场可能表现更好
            adjusted_weights['lr'] *= 1.2
            adjusted_weights['rf'] *= 0.9
            adjusted_weights['gb'] *= 0.9
            
        elif current_state == 1 or current_state == 2:  # 趋势市场
            # 集成方法在趋势市场表现更好
            adjusted_weights['rf'] *= 1.1
            adjusted_weights['gb'] *= 1.1
            adjusted_weights['lr'] *= 0.8
            
        elif current_state == 3:  # 高波动市场
            # 随机森林在高波动环境下更稳健
            adjusted_weights['rf'] *= 1.3
            adjusted_weights['gb'] *= 0.8
            adjusted_weights['lr'] *= 0.7
        
        # 归一化权重
        total_weight = sum(adjusted_weights.values())
        if total_weight > 0:
            adjusted_weights = {name: weight / total_weight 
                              for name, weight in adjusted_weights.items()}
        
        return adjusted_weights

    def _extract_feature_importance(self, models: Dict, feature_names: list):
        """提取特征重要性"""
        
        self.feature_importance = {}
        
        for name, model in models.items():
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
                self.feature_importance[name] = dict(zip(feature_names, importance))
            elif hasattr(model, 'coef_'):
                # 线性模型使用系数的绝对值作为重要性
                importance = np.abs(model.coef_[0] if model.coef_.ndim > 1 else model.coef_)
                self.feature_importance[name] = dict(zip(feature_names, importance))
        
        # 计算集成特征重要性
        if self.feature_importance:
            ensemble_importance = {}
            for feature in feature_names:
                importance_values = []
                for name, importance_dict in self.feature_importance.items():
                    if feature in importance_dict:
                        weight = self.model_weights.get(name, 0)
                        importance_values.append(weight * importance_dict[feature])
                
                ensemble_importance[feature] = sum(importance_values) if importance_values else 0
            
            self.feature_importance['ensemble'] = ensemble_importance
            
            # 记录最重要的特征
            top_features = sorted(ensemble_importance.items(), key=lambda x: x[1], reverse=True)[:10]
            logger.info(f"Top 10 important features: {top_features}")

    def save(self, path: str):
        """保存模型"""
        model_data = {
            'trained_models': self.trained_models,
            'model_weights': self.model_weights,
            'selected_features': getattr(self, 'selected_features', []),
            'feature_importance': self.feature_importance,
            'model_performance': self.model_performance,
            'market_state_classifier': self.market_state_classifier,
            'state_features': getattr(self, 'state_features', [])
        }
        joblib.dump(model_data, path)
        logger.info(f"AI Agent Ensemble model saved to {path}")

    def load(self, path: str):
        """加载模型"""
        try:
            model_data = joblib.load(path)
            self.trained_models = model_data.get('trained_models', {})
            self.model_weights = model_data.get('model_weights', self.model_weights)
            self.selected_features = model_data.get('selected_features', [])
            self.feature_importance = model_data.get('feature_importance', {})
            self.model_performance = model_data.get('model_performance', self.model_performance)
            self.market_state_classifier = model_data.get('market_state_classifier')
            self.state_features = model_data.get('state_features', [])
            logger.info(f"AI Agent Ensemble model loaded from {path}")
            return self
        except Exception as e:
            logger.error(f"Error loading model from {path}: {e}")
            raise
