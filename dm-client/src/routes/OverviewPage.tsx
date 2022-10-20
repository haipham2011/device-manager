import { useState } from "react";
import Loading from "../components/Loading";
import Modal from "../components/Modal";
import { SystemDevice } from "../models/overview";
import { useGetOverviewQuery } from "../services/deviceManager";

export default function OverviewPage() {
  const { data, isLoading } = useGetOverviewQuery("");
  const [modalOn, setModalOn] = useState(false);
  const [chosenDevice, setChosenDevice] = useState<SystemDevice | null>(null)

  const clicked = (element: SystemDevice) => {
    setModalOn(true)
    setChosenDevice(element)
  }

  return isLoading ? (
    <Loading /> 
  ) : (
    <div className="fixed h-screen" style={{ marginLeft: "255px"}}>
      <div className="flex items-center justify-center bg-gray-400 h-screen">
        <div className="grid grid-cols-4 gap-4 grid-flow-row ">
          <div className="p-20 text-left bg-white col-start-1 col-end-5">
            <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl">
              {data.system.name}
            </h1>
          </div>
          <div className="pl-15 bg-white">
            <img
              className="object-cover w-full h-full rounded-t-lg md:h-100 md:w-auto md:rounded-none md:rounded-l-lg"
              src={`${data.system.image}`}
              alt=""
            />
          </div>
          <div className="p-5 text-left bg-white col-start-2 col-end-5">
            <h2 className="text-4xl font-extrabold">General information</h2>
            <p className="mb-4 text-lg font-normal text-gray-500">
              <b>Version:</b> {data.version}
            </p>
            <p className="mb-4 text-lg font-normal text-gray-500">
              <b>Company:</b> {data.company}
            </p>
            <p className="mb-4 text-lg font-normal text-gray-500">
              <b>Location:</b> {data.location}
            </p>
            <p className="mb-4 text-lg font-normal text-gray-500">
              <b>Code:</b> {data.system.code}
            </p>
            <p className="mb-4 text-lg font-normal text-gray-500">
              <b>Description:</b> {data.system.description}
            </p>
          </div>
          {data.devices.map((element: SystemDevice) => (
            <div className="pl-15 bg-white" onClick={() => clicked(element)} key={element.id}>
              <a className="flex flex-col items-center bg-white rounded-lg border shadow-md md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700">
                <div className="flex flex-col justify-between p-4 leading-normal">
                  <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                    {element.name}
                  </h5>
                  <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
                    {element.code}
                  </p>
                  <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
                    {element.provider}
                  </p>
                </div>
              </a>
            </div>
          ))}
          {modalOn && chosenDevice && < Modal setModalOn={setModalOn} elementId={chosenDevice.id} />}
        </div>
      </div>
    </div>
  );
}
