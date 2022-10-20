import { useGetDeviceQuery } from "../services/deviceManager";
import Loading from "./Loading";

const Modal = ({
  setModalOn,
  elementId,
}: {
  setModalOn: (state: boolean) => void;
  elementId: number
}) => {

  const handleCloseClick = () => {
    setModalOn(false);
  };
  const { data, isLoading } = useGetDeviceQuery(elementId);
  return (
    isLoading ?  <Loading /> :
    <div className="opacity-90 fixed inset-0 z-50   ">
      <div className="flex h-screen justify-center items-center ">
        {<div className="flex-col justify-center bg-white py-12 px-24 border-4 rounded-xl ">
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Code:</b> {data.code}
              </p>
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Name:</b> {data.name}
              </p>
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Size:</b> {data.size}
              </p>
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Provider:</b> {data.provider}
              </p>
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Weight:</b> {data.weight}
              </p>
              <p className="mb-4 text-lg font-normal text-gray-500">
                <b>Description:</b> {data.description}
              </p>
          <div className="flex">
            <button
              onClick={handleCloseClick}
              className="rounded px-4 py-2 ml-4 text-white bg-blue-500 "
            >
              Close
            </button>
          </div>
        </div>}
      </div>
    </div>
  );
};

export default Modal;
