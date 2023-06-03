const mongoose = require('mongoose');

const productoSchema = new mongoose.Schema({
  id: {type: String, required: true},
  name: {type: String, required: true},
  costo: {type: String, required: true},
  precio: {type: String, required: true},
  precioDesc: {type: String, required: true},
  imagen: {type: String}
}, { versionKey: false })

module.exports = mongoose.model('producto', productoSchema)