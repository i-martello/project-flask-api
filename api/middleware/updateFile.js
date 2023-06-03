const multer = require("multer");
const path = require("path");
const fs = require("fs");
const excelReader = require("../excel/ExcelReader");

const rutaUploads = path.resolve(__dirname, "../uploads")

const deleteFile = () => {
  fs.readdir(rutaUploads, (err, files) => {
    if (err) {
      console.log(err);
      return;
    }
    files.forEach(async(file, index) => {
      const extPath = path.extname(file);
      const rutacompleta = path.resolve(rutaUploads, file);
      if (extPath === ".xlsx") {
        await fs.unlink(rutacompleta, (err) => {
          if (err) {
            console.log(err);
            return;
          }
        });
        console.log(`Archivo ${file} eliminado`);
      }
    });
  });
};

const upload = multer({
  storage: multer.diskStorage({
    destination: rutaUploads,
    filename: (req, file, cb) => {
      deleteFile();
      const fileExtension = path.extname(file.originalname);
      const fileName = file.originalname.split(fileExtension)[0];
      const excelName = `${fileName}-${Date.now()}${fileExtension}`
      cb(null, excelName);
    },
  }),
});

module.exports = upload;
