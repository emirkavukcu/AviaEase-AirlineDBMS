"use client";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Seatmap from "@/components/Seatmap/Seatmap";
import BasicTable from "@/components/Tables/BasicTable";
import ExtendedTable from "@/components/Tables/ExtendedTable";
import React, { useEffect, useState } from "react";

const FlightDetailsPage = ({
  params,
}: {
  params: { flightNumber: number };
}) => {
  const [view, setView] = useState("tabular");

  const [passengersPlane, setPassengersPlane] = useState([]);
  const [passengersBasic, setPassengersBasic] = useState([]);
  const [passengersExtended, setPassengersExtended] = useState([]);
  const [flightDetails, setFlightDetails] = useState({} as any);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPassengers = async () => {
      try {
        console.log("fetching 1");
        const [planeResponse, basicResponse, extendedResponse, flightResponse] =
          await Promise.all([
            fetch(
              `http://127.0.0.1:5000/api/${params.flightNumber}/plane_view`,
            ),
            fetch(
              `http://127.0.0.1:5000/api/${params.flightNumber}/tabular_view`,
            ),
            fetch(
              `http://127.0.0.1:5000/api/${params.flightNumber}/extended_view`,
            ),
            fetch(
              `http://127.0.0.1:5000/api/flights?flight_number=${params.flightNumber}`,
            ),
          ]);
        console.log("fetching 2");
        console.log("flight response", flightResponse);
        const [planeData, basicData, extendedData, flightData] =
          await Promise.all([
            planeResponse.json(),
            basicResponse.json(),
            extendedResponse.json(),
            flightResponse.json(),
          ]);
        setPassengersPlane(planeData);
        setPassengersBasic(basicData);
        setPassengersExtended(extendedData);
        setFlightDetails(flightData.flights[0]);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching passengers:", error);
        setIsLoading(false);
      }
    };

    fetchPassengers();
  }, [params.flightNumber]);

  console.log("plane data", passengersPlane);
  console.log("basic data", passengersBasic);
  console.log("extended data", passengersExtended);
  console.log("flight data", flightDetails);

  if (isLoading) {
    return <div></div>;
  }

  return (
    <DefaultLayout>
      <div className="mt-8 w-auto rounded-lg border border-stroke bg-white px-5 pb-4 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-5">
        <h2 className=" text-2xl font-semibold text-black dark:text-white">
          Flight Details
        </h2>
        <div className="bg mt-4 flex text-lg text-black">
          <div className="flex flex-col gap-4">
            <div className="mb-2 flex flex-row gap-10">
              <div>
                <span className="font-semibold">Flight Number:</span>{" "}
                {flightDetails.flight_number}
              </div>
              <div>
                <span className="font-semibold">Flight Date:</span>{" "}
                {new Date(flightDetails.date_time).toLocaleString("en-GB", {
                  day: "2-digit",
                  month: "2-digit",
                  year: "2-digit",
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>
              <div>
                <span className="font-semibold">Distance:</span>{" "}
                {flightDetails.distance} km
              </div>
              <div>
                <span className="font-semibold">Duration:</span>{" "}
                {flightDetails.duration} hours
              </div>
            </div>
            <div className="flex flex-row gap-10">
              <div>
                <span className="font-semibold">Source Airport:</span>{" "}
                {flightDetails.source_airport}
                <div className="">
                  <span className="font-semibold">Country:</span>{" "}
                  {flightDetails.source_country}
                </div>
                <div className="">
                  <span className="font-semibold">City:</span>{" "}
                  {flightDetails.source_city}
                </div>
              </div>
              <div>
                <span className="font-semibold">Destination Airport:</span>{" "}
                {flightDetails.destination_airport}
                <div className="">
                  <span className="font-semibold">Country:</span>{" "}
                  {flightDetails.destination_country}
                </div>
                <div className="">
                  <span className="font-semibold">City:</span>{" "}
                  {flightDetails.destination_city}
                </div>
              </div>
              <div>
                <span className="font-semibold">Aircraft Type:</span>{" "}
                {flightDetails.aircraft_type}
              </div>
              <div>
                <span className="font-semibold">Status:</span>{" "}
                {flightDetails.status}
              </div>
            </div>
          </div>
          <div className="ml-8">
            <div>
              <span className="font-semibold">Flight Menu:</span>
              <ul className="ml-4 mt-2 grid list-disc grid-cols-1 gap-x-10 sm:grid-cols-2 lg:grid-cols-2">
                {flightDetails.flight_menu.map(
                  (item: string, index: number) => (
                    <li key={index}>{item}</li>
                  ),
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-4 p-3">
        <div
          className="inline-flex cursor-pointer items-center  justify-center rounded-full bg-primary px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={() => setView("tabular")}
        >
          Tabular View
        </div>
        <div
          className="inline-flex cursor-pointer items-center justify-center rounded-full bg-primary px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={() => setView("extended")}
        >
          Extended View
        </div>
      </div>
      <div className="flex justify-center">
        {view === "tabular" && (
          <div className="mr-10">
            <BasicTable passengers={passengersBasic} />
          </div>
        )}
        {view === "extended" && (
          <div className="mr-10 w-3/4">
            <ExtendedTable roster={passengersExtended} />
          </div>
        )}
        <div>
          <Seatmap passengers={passengersPlane} />
        </div>
      </div>
    </DefaultLayout>
  );
};

export default FlightDetailsPage;
