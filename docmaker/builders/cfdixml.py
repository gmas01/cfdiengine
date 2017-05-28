import datetime
import pyxb
import psycopg2.extras

from sat.v33 import Comprobante
from sat.requirement import writedom_cfdi

class CfdiXml(BuilderGen):

    def __init__(self, logger):
        super().__init__(logger)

    def __q_moneda(self, conn, prefact_id):
        SQL = """SELECT
            gral_mon.iso_4217 AS curr_iso_4217,
            gral_mon.simbolo AS curr_symbol,
            erp_prefacturas.tipo_cambio
            FROM erp_prefacturas
            LEFT JOIN gral_mon ON gral_mon.id=erp_prefacturas.moneda_id
            WHERE erp_prefacturas.id="""
        return self.pg_query(conn, "{0}'{1}'".format(SQL, prefact_id))

    def __q_receptor(self, conn, prefact_id):
        SQL = """SELECT
            cxc_clie.razon_social,
            cxc_clie.rfc
            FROM erp_prefacturas
            LEFT JOIN cxc_clie ON cxc_clie.id=erp_prefacturas.cliente_id
            WHERE erp_prefacturas.id="""
        return self.pg_query(conn, "{0}'{1}'".format(SQL, prefact_id))

    def __q_conceptos(self, conn, prefact_id):
        '''
        Busca los conceptos a facturar de la prefactura en dbms
        '''
        SQL = """SELECT inv_prod.sku, inv_prod.descripcion,
            inv_prod_unidades.titulo AS unidad,
            erp_prefacturas_detalles.cant_facturar AS cantidad,
            erp_prefacturas_detalles.precio_unitario,
            (erp_prefacturas_detalles.cant_facturar * erp_prefacturas_detalles.precio_unitario) AS importe
            FROM erp_prefacturas
            JOIN erp_prefacturas_detalles on erp_prefacturas_detalles.prefacturas_id=erp_prefacturas.id
            LEFT JOIN inv_prod on inv_prod.id = erp_prefacturas_detalles.producto_id
            LEFT JOIN inv_prod_unidades on inv_prod_unidades.id = erp_prefacturas_detalles.inv_prod_unidad_id
            WHERE erp_prefacturas_detalles.prefacturas_id="""
        return self.pg_query(conn, "{0}'{1}'".format(SQL, prefact_id))

    def data_acq(self, conn, d_rdirs, **kwargs):
        pass

    def format_wrt(self, output_file, dat):
        c = Comprobante()
        c.Version = '3.3'
        c.Folio = "test attribute" #optional
        c.Fecha = '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.datetime.now())
        c.Sello = "BLABLALASELLO"
        c.FormaPago = "01" #optional
        c.NoCertificado = "00001000000202529199"
        c.Certificado = "certificado en base64"
        c.SubTotal = "4180.0"
        c.Total = "4848.80"
        c.Moneda = "MXN"
        c.TipoCambio = "1.0" #optional (requerido en ciertos casos)
        c.TipoDeComprobante = 'I'
    #    c.metodoDePago = "NO IDENTIFICADO" #optional
        c.LugarExpedicion = "60050"

        c.Emisor = pyxb.BIND()
        c.Emisor.Nombre = "PRODUCTOS INDUSTRIALES SAAR S.A. DE C.V." #opcional
        c.Emisor.Rfc = "PIS850531CS4"
        c.Emisor.RegimenFiscal = '601'

        c.Receptor = pyxb.BIND()
        c.Receptor.Nombre = "PRODUCTOS INDUSTRIALES SAAR S.A. DE C.V." #opcional
        c.Receptor.Rfc = "PIS850531CS4"
        c.Receptor.UsoCFDI = 'G01'

        c.Conceptos = pyxb.BIND(
            pyxb.BIND(
                Cantidad=5,
                ClaveUnidad='C81',
                ClaveProdServ='01010101',
                Descripcion='Palitroche',
                ValorUnitario='10',
                Importe='50'
            )
        )

        writedom_cfdi(c.toDOM(), output_file)

    def data_rel(self, dat):
        pass
