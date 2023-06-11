declare module 'react-json-to-excel' {
  const ReactJsonToExcel: any;

  const ReactJsonToExcel: ComponentType<ReactJsonToExcelProps>;
  const exportToExcel: (data: any[], fileName?: string, fields?: { key: string; label: string }[]) => void;
  
  export { exportToExcel };
  export default ReactJsonToExcel;
}
