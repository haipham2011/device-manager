import { useEffect } from "react";
import { useGetMessagesQuery } from "../services/deviceManager";
import { useSelector } from "react-redux";
import { RootState } from "../store";
import Loading from "../components/Loading";

export default function DiagnosticsPage() {
  const { data, isLoading, refetch } = useGetMessagesQuery("");
  const count = useSelector((state: RootState) => state.messageCounter.value);

  useEffect(() => {
    refetch();
  }, [count]);

  return isLoading ? (
    <Loading /> 
  ) : (
    <div className="w-full overflow-auto" style={{ marginLeft: "255px" }}>
      <div className="flex w-full overflow-x-auto items-center justify-center relative">
        <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" className="py-3 px-6">
                ID
              </th>
              <th scope="col" className="py-3 px-6">
                Type
              </th>
              <th scope="col" className="py-3 px-6">
                Time
              </th>
              <th scope="col" className="py-3 px-6">
                Status
              </th>
              <th scope="col" className="py-3 px-6">
                Machine ID
              </th>
            </tr>
          </thead>
          <tbody>
            {data && data["messages"] && data["messages"].map((element) => (
              <tr className="bg-white" key={element.id + "-" + element.machineId}>
                <td className="py-4 px-6">{element.id}</td>
                <td className="py-4 px-6">{element.type}</td>
                <td className="py-4 px-6">{element.time}</td>
                <td className="py-4 px-6">{element.status}</td>
                <td className="py-4 px-6">{element.machineId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
