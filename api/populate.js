require("dotenv").config();
const fs = require("fs");
const path = require("path");
const connectDB = require("./db/connect");
const productoSchema = require("./models/product");

connectDB(process.env.MONGO_URI, console.log("Mongo funcionando"));

const rutaProductos = path.resolve(__dirname, "productos.txt");
const productosTxt = fs.readFile(rutaProductos, "utf-8", async (err, data) => {
  const arrayLines = data.split(/\n/);
  await productoSchema.deleteMany({});
  for (item of arrayLines) {
    arrayFields = item.split(/\t/);
    const imagen = arrayFields[0].replace("-", "");
    await new productoSchema({
      id: arrayFields[0],
      name: arrayFields[1],
      costo: arrayFields[2],
      precio: arrayFields[3],
      imagen: `https://www.papelerabariloche.com.ar/img/p/${imagen}/1.jpeg?quality=95&width=800&height=800&mode=max&upscale=false&format=webp`,
    })
      .save()
      .then("Precios Actualizados")
      .catch("Error");
  }
});
console.log(rutaProductos);
