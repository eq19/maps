/**
 * Exemplo de `Strategy` baseada no indicador `tulip-adx` com controle de stoploss
 *
 * Conceitos básicos:
 * trend long = compra
 * trend short = venda
 *
 */
var method = {};

// Prepara a estratégia
method.init = function () {
  // Nome da Estratégia
  this.name = 'tulip-adx-custom';
  // Indica se a estratégia está inclinada para venda (short) ou compra (long)
  this.trend = 'none';
  // Recupera do TradingAdvisor o número de históricos necessários para calcular os indicadores
  this.requiredHistory = this.tradingAdvisor.historySize;
  // Cria o indicador de ADX com nome `myadx`
  this.addTulipIndicator('myadx', 'adx', this.settings);

  // Indicador StopLoss para essa estratégia
  // TODO recuperar da configuração de cada usuário, chamar uma biblioteca de stoploss pode ser o mais interessante
  // XXX criar uma biblioteca no core do Gekko que permita importar abstrações como stoploss
  this.stopLossIndicator = this.settings.general.stopLoss || 1;
  this.stop = "";
};

// What happens on every new candle?
method.update = function (candle) {
  // do nothing!
};

method.log = function () {
  // do nothing!
}

// Lógica da Estratégia
method.check = function (candle) {

  // Preço Atual
  var price = candle.close;

  // Resultado ADX baseado no indicador e no histórico
  var adx = this.tulipIndicators.myadx.result.result;

  // Indicador DOWN > ADX + Trend Long or None
  if (this.settings.thresholds.down > adx && this.trend !== 'short' || this.stop != "" && price < this.stop) {

    // Log que o Stop Loss foi acionado
    if(this.stop != "" && price<this.stop){
      console.log("stoplosss triggered - "+ this.stop, price);
    }

    // O Advice é de Venda então o stop loss é zerado
    if (this.trend == 'long') {
      console.info('advise de vebda stop loss zerado')
      this.stop = "";
    }

    // Advice de venda pois o ADX bateu a marca
    this.trend = 'short';
    this.advice('short');

    // Indicador UP < ADX + Trend Long or None
  } else if (this.settings.thresholds.up < adx && this.trend !== 'long') {
    
    // O Advice é de Compra, então seta um stoploss
    if (this.stop == "") {

      this.stop = price - (price * this.stopLossIndicator);
      this.trend = 'long';

      // Envia advice de compra
      this.advice('long');

    }
  }
}

module.exports = method;
