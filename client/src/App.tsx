import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { exportToExcel } from "react-json-to-excel";

interface productoType {
  _id: string;
  codigo: string;
  articulo: string;
  costo: string;
  precio: string;
  fecha: string;
  imagen: string;
}

interface dolarBlueType {
  value_avg: number;
  value_buy: number;
  value_sell: number;
}

const App = () => {
  const [productos, setProductos] = useState<productoType[]>([]);
  const [preciosExcel, setPreciosExcel] = useState([]);
  const [buscador, setBuscador] = useState<string>("");
  const [dolarBlue, setDolarBlue] = useState<dolarBlueType>({
    value_avg: 0,
    value_buy: 0,
    value_sell: 0,
  });
  const [archivoActualizar, setArchivoActualizar] = useState<File>();

  useEffect(() => {
    (async () => {
      await axios.get("https://precioscopyart-api.vercel.app/api/getall")
      .then(res => setProductos(JSON.parse(res.data)))
      .catch(err => console.log(err))
    })();
  }, []);

  useEffect(() => {
    (async () => {
      await axios
        .get("https://api.bluelytics.com.ar/v2/latest")
        .then((res) => setDolarBlue(res.data.blue))
        .catch((err) => console.log(err));
    })();
  }, [dolarBlue]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await axios
      .get("https://precioscopyart-api.vercel.app/api/v1/productos", {
        params: { search: buscador },
      })
      .then((res) => setProductos(res.data.documentos));
    setBuscador("");
  };

  const changeUpdate = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setArchivoActualizar(e.target.files[0]);
    }
  };

  const handleUpdate = async () => {
    // if (archivoActualizar) {
    //   const data = new FormData();
    //   data.append("file", archivoActualizar!);
    //   await axios({method: "post", url: "https://precioscopyart-api.vercel.app/api/upload", responseType: "blob", data })
    //   .then(response => {
    //     const url = URL.createObjectURL(response.data);

    //     const link = document.createElement('a');
    //     link.href = url;
    //     link.download = 'precios.xlsx';
    //     link.click();
    //   })

    // }
    if (archivoActualizar) {
      const data = new FormData();
      data.append("file", archivoActualizar!);
      await axios({method: "post", url: "https://precioscopyart-api.vercel.app/api/upload", data })
      .then(response => setPreciosExcel(JSON.parse(response.data)))
      exportToExcel(preciosExcel, 'precios_excel')
    }
    
  };


  return (
    <div>
      <div className="my-5 mx-auto w-[50%]">
        <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Actualizar Precios
        </label>
        <div className="flex items-center border-solid border-black">
          <input
            className="block w-full text-sm text-gray-900 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            id="file_input"
            type="file"
            onChange={changeUpdate}
          />
          <button
            type="submit"
            className="font-bold mx-2"
            onClick={handleUpdate}
          >
            Actualizar
          </button>
        </div>
      </div>
      <div>
        <form onSubmit={handleSubmit}>
          <label className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">
            Buscar producto
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <svg
                aria-hidden="true"
                className="w-5 h-5 text-gray-500 dark:text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                ></path>
              </svg>
            </div>
            <input
              type="search"
              id="search"
              className="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="Buscar"
              required
              onChange={(e) => setBuscador(e.target.value)}
              value={buscador}
            />
            <button
              type="submit"
              className="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Buscar
            </button>
          </div>
        </form>
      </div>
      <div className="relative overflow-y-auto shadow-md sm:rounded-lg my-[5%]">
        <table className="w-full text-lg text-left text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" className="px-6 py-3">
                Imagen
              </th>
              <th scope="col" className="px-6 py-3">
                Id
              </th>
              <th scope="col" className="px-6 py-3">
                Producto
              </th>
              <th scope="col" className="px-6 py-3">
                Costo
              </th>
              <th scope="col" className="px-6 py-3">
                Precio
              </th>
              <th scope="col" className="px-6 py-3">
                Fecha
              </th>
            </tr>
          </thead>
          <tbody>
            {productos.map((producto) => {
              return (
                <tr className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                  <td className="px-6 py-4 w-[150px] h-[150px]">
                    <img
                      className="w-full h-full"
                      src={producto.imagen}
                      alt={producto.articulo}
                    />
                  </td>
                  <td
                    scope="row"
                    className="px-6 py-4 font-medium whitespace-nowrap dark:text-white"
                  >
                    {producto.codigo}
                  </td>
                  <td className="px-6 py-4 text-gray-900">{producto.articulo}</td>
                  <td className="px-6 py-4 text-gray-900">{producto.costo}</td>
                  <td className="px-6 py-4 font-bold text-gray-900">
                    {producto.precio}
                  </td>
                  <td className="px-6 py-4 text-gray-900">
                    {producto.fecha}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="absolute left-[72%] top-[2%]">
        <div className="min-w-0 rounded-lg shadow-xs overflow-hidden bg-white dark:bg-gray-800">
          <div className="p-4 justify-center flex items-center">
            <div className="p-3 rounded-full text-green-500 dark:text-green-100 bg-green-100 dark:bg-green-500 mr-4">
              <svg fill="currentColor" viewBox="0 0 20 20" className="w-5 h-5">
                <path
                  fill-rule="evenodd"
                  d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                  clip-rule="evenodd"
                ></path>
              </svg>
            </div>
            <div>
              <p className="mb-2 flex items-center text-sm font-medium text-gray-600 dark:text-gray-400">
                Dolar Blue
              </p>
              <p className="text-lg font-semibold text-gray-700 dark:text-gray-200">
                $ {dolarBlue.value_sell}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
