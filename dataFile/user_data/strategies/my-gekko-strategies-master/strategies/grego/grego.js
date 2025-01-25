/**
 * Exemplo
 * 
 * Executar uma ordem, quando ensta em baixa. 
 * E vender quando está em alta.
 *
 * Conceitos básicos:
 * trend long = compra = this.advice("long");
 * trend short = venda =  this.advice("short");
 * 
 * baixaCompra = 0.98
 * vendaAlta = 1.03
 *
 */
var method = {};

var valorQueEuQueroComprar = 0.0;
var valorMaisBaixo = 0.0;
var valorDeVenda = 0.0;
var adviced = false;

// Prepara a estratégia
method.init = function () {
    this.name = 'grego';
    this.percentCompraBaixa = this.settings.percentCompraBaixa;
    this.percentVendaAlta = this.settings.percentVendaAlta;
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

    if (valorQueEuQueroComprar == 0) {
        valorQueEuQueroComprar = candle.close * this.percentCompraBaixa;
    }

    if (candle.close <= valorQueEuQueroComprar) {
        valorMaisBaixo = candle.close;
    }

    // console.info(`candle.close=${candle.close} > valorMaisBaixo=${valorMaisBaixo} && !adviced=${adviced} = (${candle.close > valorMaisBaixo && !adviced})`)
    if(candle.close > valorMaisBaixo && !adviced){
        this.advice("long"); // compra
        valorDeVenda = candle.close * this.percentVendaAlta;
        adviced = true;
    }
    console.info(`candle.close=${candle.close} > valorDeVenda=${valorDeVenda} = ${candle.close > valorDeVenda}`);
    if(candle.close > valorDeVenda){
        this.advice("short"); // venda
        valorQueEuQueroComprar = 0;
        valorMaisBaixo = 0;
        valorDeVenda = 0;
        adviced = false;
    }
}

module.exports = method;
