const express = require('express');
const connectDB = require('./db/connect');
const router = require('./routes/products');
const cors = require('cors')
require('dotenv').config()

const app = express();

const PORT = process.env.PORT || 3000

app.use(cors());
app.use(express.json());
app.use('/api/v1/productos', router);

try {
  connectDB(process.env.MONGO_URI);
  app.listen(PORT, () => console.log(`Server funcionando en el puerto ${PORT}`));
} catch (error) {
  console.log(error);
}