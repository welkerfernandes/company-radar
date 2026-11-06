export type Field = {name:string;label:string;type?:string;options?:{value:string;label:string}[]};
export const config: {title:string;symbol:string;subtitle:string;headline:string;description:string;provider:string;source:string;notice:string;defaults:Record<string,string>;fields:Field[]} = {
  "title": "Company Radar",
  "symbol": "◎",
  "subtitle": "Corporate registry monitoring",
  "headline": "Evidências antes de aprovar.",
  "description": "Consulte cadastros públicos e acompanhe a consistência dos fornecedores.",
  "provider": "BrasilAPI",
  "source": "https://brasilapi.com.br/docs",
  "notice": "Consistência cadastral não é aprovação de crédito, fraude ou conformidade. Apenas CNPJ numérico é suportado.",
  "defaults": {
    "cnpj": "00.000.000/0001-91"
  },
  "fields": [
    {
      "name": "cnpj",
      "label": "CNPJ do fornecedor",
      "type": "text"
    }
  ]
};
