const fs = require("fs");
const path = require("path");
const _ = require('lodash');
const excelReader = require("../excel/ExcelReader");
const productoSchema = require("../models/product");
const ctrlUpdate = {};

ctrlUpdate.add = async (req, res) => {
  rutaExcel = path.resolve(__dirname, "../uploads");
  fs.readdir(rutaExcel, (err, files) => {
    if (err) {
      console.log(err);
      return;
    }
    excelReader(files[0], async (err, productos) => {
      if (err) {
        console.log(err);
        return;
      }
      await productoSchema.deleteMany({});
      for(producto of productos){
        const idNumber = producto.__EMPTY_1.replace('-','');
        const imagen = `https://www.papelerabariloche.com.ar/img/p/${idNumber}/1.jpeg?quality=95&width=800&height=800&mode=max&upscale=false&format=webp`
        const calculoVenta = (producto.__EMPTY_3 / 1.21) * 1.105
        const precioVenta = Math.round(calculoVenta * 1.5);
        const nombreProductos = _.deburr(producto.__EMPTY_2)
        const productObject = {
          id: producto.__EMPTY_1,
          name: producto.__EMPTY_2,
          costo: producto.__EMPTY_3,
          precio: precioVenta,
          imagen
        }

        await new productoSchema({
          id: producto.__EMPTY_1,
          name: nombreProductos,
          costo: `$${Math.round(producto.__EMPTY_3)}`,
          precio: `$${Math.round(producto.__EMPTY_3 * 1.5)}`,
          precioDesc: `$${precioVenta}`,
          imagen
        }).save();
      };
    });
  });
  res.end();
};

module.exports = ctrlUpdate;
