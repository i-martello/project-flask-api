const productoSchema = require('../models/product');

const ctrlProduct = {}


ctrlProduct.getStatic = async (req, res)=> {
  const variabless = 'cuader'
  const productos = await productoSchema.find({name: { $regex: 'cuade', $options: 'i' }});
  res.json({productos});
}

ctrlProduct.getAll = async (req, res)=>{

  let skip = 0
  let limit = 50
  let documentos = []

  const obtenerDatos = async ()=>{
    let filtros = {}
    if(req.query.search){
      const { search } = req.query
      const palabras = search.split(' ');
      const condiciones = palabras.map( palabra => ({name: { $regex: palabra, $options: 'i'}}));
      filtros = { $and: condiciones}
    }
    const productos = await productoSchema.find(filtros).skip(skip).limit(limit);

    documentos = documentos.concat(productos);
    skip += limit
    if(limit === productos.length){
      await obtenerDatos();
    } else {
      res.json({documentos});
    }
  }
  obtenerDatos()

}

module.exports = ctrlProduct;