const XLSX = require("xlsx");
const fs = require("fs");
const path = require("path");

const rutaCodigos = path.resolve(__dirname, "../codigos.txt");

const excelReader = (filename, callback) => {
  fs.readFile(rutaCodigos, "utf-8", (err, file) => {
    if (err) {
      console.log(err);
    }

    const arrayCodigos = file.split(/\s+/);

    const workbook = XLSX.readFile(`./uploads/${filename}`);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];

    const filas = XLSX.utils.sheet_to_json(worksheet);

    var productos = [];

    arrayCodigos.forEach((codigo) => {
      const producto = filas.find((fila) => fila.__EMPTY_1 == codigo);
      if (producto) {
        productos.push(producto);
      }
    });
      callback(null, productos)
  });
};

module.exports = excelReader;
