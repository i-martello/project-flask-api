import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { exportToExcel } from "react-json-to-excel";

interface productoType {
  _id: string;
  CODIGO: string;
  imagen: string;
  ARTICULO: string;
  c_iva: string;
  COSTO: string;
  VENTA: string;
  DTO: string;
  FECHA: string;
}

interface dolarBlueType {
  value_avg: number;
  value_buy: number;
  value_sell: number;
}

const App = () => {
  const [productos, setProductos] = useState<productoType[]>([]);
  const [buscador, setBuscador] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [background, setBackground] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [manualForm, setManualForm] = useState(false);
  const [dolarBlue, setDolarBlue] = useState<dolarBlueType>({
    value_avg: 0,
    value_buy: 0,
    value_sell: 0,
  });

  useEffect(() => {
    (async () => {
      await axios
        .get(`http://localhost:5000/api/getall`)
        .then((res) => setProductos(JSON.parse(res.data)))
        .catch((err) => console.log(err));
    })();
  }, []);

  useEffect(() => {
    (async () => {
      await axios
        .get("http://api.bluelytics.com.ar/v2/latest")
        .then((res) => setDolarBlue(res.data.blue))
        .catch((err) => console.log(err));
    })();
  }, [dolarBlue]);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await axios
      .get(`http://localhost:5000/api/search`, {
        params: { search: buscador },
      })
      .then((res) => setProductos(JSON.parse(res.data)));
    setBuscador("");
  };

  const handleUpdate = async () => {
    setBackground(true);
    setLoading(true);
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
    await axios({
      method: "get",
      url: `http://localhost:5000/api/upload`,
    })
      .then((response) => {
        console.log(response);

        const currentDate = new Date();
        // Formatear la fecha
        const formattedDate = currentDate.toISOString().slice(0, 10);

        // Generar el nombre del archivo con la fecha actual
        const fileName = `precios_${formattedDate}.txt`;
        exportToExcel(JSON.parse(response.data), fileName);
        setLoading(false);
        setBackground(false)
      })
      .catch(() => {
        console.log("reintentando...");

        handleUpdate();
      });
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  }
  const handleManualUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!selectedFile) {
      alert('Por favor suba un archivo.');
      return;
  }
  const formData = new FormData();
  formData.append('file', selectedFile);
  
  try {
    await axios.post('http://localhost:5000/api/manual_upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((response)=>{
      console.log(response);

      const currentDate = new Date();
      // Formatear la fecha
      const formattedDate = currentDate.toISOString().slice(0, 10);

      // Generar el nombre del archivo con la fecha actual
      const fileName = `precios_${formattedDate}.txt`;
      exportToExcel(JSON.parse(response.data), fileName);
    })
    // Aquí puedes manejar la respuesta del servidor
  } catch (error) {
    console.error('Error uploading file:', error);
    // Aquí puedes manejar el error en caso de que ocurra
  }
  }
  return (
    <div>
      <div
        className={`${
          background ? "visible" : "invisible"
        } fixed top-0 z-50 left-0 w-full h-full flex flex-col items-center justify-center bg-black bg-opacity-50`}
      >
        <div className={`${loading ? "visible" : "invisible"} absolute top-[45%] left-[45%]`}>
          <div className="mb-4 text-white text-lg">
            Descargando lista de precios...
          </div>
          <div className="m-auto w-24 h-24 border-t-4 border-blue-500 border-solid rounded-full animate-spin"></div>
        </div>
        <div
          className={`${
            manualForm ? "visible" : "invisible"
          } flex justify-center items-center w-screen h-screen`}
        >
          <div className="relative space-y-6 w-[35%] h-[25%] py-4 mb-36 rounded-md bg-gray-500">
            <button
              type="button"
              className="absolute top-2 right-2 bg-white hover:bg-red-600 rounded-md p-2 inline-flex items-center justify-center text-gray-800 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
              onClick={()=> {setManualForm(false), setBackground(false)}}
            >
              <span className="sr-only">Close menu</span>
              <svg
                className="h-4 w-5"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
            <label className="font-medium text-2xl text-gray-900">
              Ingrese la lista de precios de Papelera Bariloche
            </label>
            <form className="space-y-6" onSubmit={handleManualUpdate}>
              <input
                className="block w-[50%] m-auto text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400"
                id="file_input"
                type="file"
                onChange={handleFileChange}
              />
                <button
                  type="submit"
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                >
                  <svg
                    className="fill-current w-4 h-4 mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                  >
                    <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" />
                  </svg>
                  <span>Download</span>
                </button>
            </form>
          </div>
        </div>
      </div>
      <div>
        <div className="my-5 mx-auto items-center">
          <div className="flex justify-between w-[60%]">
            <div className="flex items-center border-solid border-black">
              <button
                className="bg-green-500 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={handleUpdate}
              >
                <svg
                  className="fill-current w-4 h-4 mr-2"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" />
                </svg>
                <span>Descargar nueva lista</span>
              </button>
            </div>
            <div className="flex items-center border-solid border-black">
              <button
                className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
                onClick={() => {
                  setManualForm(true), setBackground(true);
                }}
              >
                <svg
                  className="fill-current w-4 h-4 mr-2"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" />
                </svg>
                <span>Obtener lista manualmente</span>
              </button>
            </div>
          </div>
        </div>
        <div>
          <form onSubmit={handleSearch}>
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
                <th scope="col" className="px-6 py-4 text-xl">
                  Imagen
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  Id
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  Producto
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  C/IVA
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  COSTO
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  VENTA
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
                  DTO.
                </th>
                <th scope="col" className="px-6 py-4 text-xl">
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
                        alt={producto.ARTICULO}
                      />
                    </td>
                    <td
                      scope="row"
                      className="px-6 py-4 font-medium whitespace-nowrap dark:text-white"
                    >
                      {producto.CODIGO}
                    </td>
                    <td className="px-6 py-4 text-gray-900">
                      {producto.ARTICULO}
                    </td>
                    <td className="px-6 py-4 text-gray-900">
                      {producto.c_iva}
                    </td>

                    <td className="px-6 py-4 text-gray-900">
                      {producto.COSTO}
                    </td>
                    <td className="px-6 py-4 font-bold text-gray-900">
                      {producto.VENTA}
                    </td>
                    <td className="px-6 py-4 text-gray-900">{producto.DTO}</td>

                    <td className="px-6 py-4 w-[150px]  text-gray-900">
                      {producto.FECHA}
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
                <svg
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  className="w-5 h-5"
                >
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
    </div>
  );
};

export default App;
