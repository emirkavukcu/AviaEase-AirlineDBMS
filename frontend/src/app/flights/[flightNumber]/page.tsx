"use client";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import SeatMap from "@/components/Seatmap/Seatmap";
import BigSeatMap from "@/components/Seatmap/BigSeatMap";
import BasicTable from "@/components/Tables/BasicTable";
import ExtendedTable from "@/components/Tables/ExtendedTable";
import React, { useEffect, useState } from "react";
import countries from "i18n-iso-countries";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

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
  const [planeData, setPlaneData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPassengers = async () => {
      try {
        const [planeResponse, basicResponse, extendedResponse, flightResponse] =
          await Promise.all([
            fetchWithAuth(
              `http://127.0.0.1:5000/api/${params.flightNumber}/plane_view`,
            ),
            fetchWithAuth(
              `http://127.0.0.1:5000/api/${params.flightNumber}/tabular_view`,
            ),
            fetchWithAuth(
              `http://127.0.0.1:5000/api/${params.flightNumber}/extended_view`,
            ),
            fetchWithAuth(
              `http://127.0.0.1:5000/api/flights?flight_number=${params.flightNumber}`,
            ),
          ]);
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
        setPlaneData(
          planeData.map(({ seniority_level, ...rest }: any) => rest),
        ); // Store planeData for download without seniority_level
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching passengers:", error);
        setIsLoading(false);
      }
    };

    fetchPassengers();
  }, [params.flightNumber]);

  const downloadJSON = (data: any, filename: any) => {
    const jsonBlob = new Blob([JSON.stringify(data)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(jsonBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const convertToSQL = (data: any) => {
    const tableName = "roster";
    const columns = Object.keys(data[0]);
    const createTableStatement = `
      CREATE TABLE ${tableName} (
        ${columns
          .map((col) =>
            col === "id" ? `${col} INTEGER` : `${col} VARCHAR(255)`,
          )
          .join(",\n  ")}
      );
          `;
    const insertStatements = data
      .map((row: any) => {
        const values = columns.map((col) => `'${row[col]}'`).join(", ");
        return `INSERT INTO ${tableName} (${columns.join(", ")}) VALUES (${values});`;
      })
      .join("\n");
    return createTableStatement + "\n" + insertStatements;
  };

  const downloadSQL = (data: any, filename: any) => {
    const sql = convertToSQL(data);
    const sqlBlob = new Blob([sql], { type: "application/sql" });
    const url = URL.createObjectURL(sqlBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadJSON = () => {
    downloadJSON(planeData, `rosterData_${params.flightNumber}.json`);
  };

  const handleDownloadSQL = () => {
    downloadSQL(planeData, `rosterData_${params.flightNumber}.sql`);
  };

  if (isLoading) {
    return <div></div>;
  }

  return (
    <DefaultLayout>
      <div className="mx-auto mt-8 w-3/4 rounded-lg border border-stroke bg-white px-5 pb-4 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark dark:text-white sm:px-7.5 xl:pb-5">
        <h2 className="text-2xl font-semibold text-black dark:text-white">
          Flight Details
        </h2>
        <div className="mt-4 grid grid-cols-1 gap-4 text-lg text-black  dark:text-white lg:grid-cols-3 lg:gap-8">
          <div className="grid grid-cols-2 gap-4 border-r pr-4 text-left dark:text-white lg:col-span-2">
            <div className="border-b pb-2">
              <span className="font-semibold dark:text-white ">
                Flight Number:
              </span>{" "}
              {flightDetails.flight_number}
            </div>
            <div className="border-b pb-2">
              <span className="font-semibold dark:text-white ">
                Flight Date:
              </span>{" "}
              {new Date(flightDetails.date_time).toLocaleString("en-GB", {
                day: "2-digit",
                month: "2-digit",
                year: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>
            <div className="border-b pb-2">
              <span className="font-semibold">Distance:</span>{" "}
              {flightDetails.distance} km
            </div>
            <div className="border-b pb-2">
              <span className="font-semibold">Duration:</span>{" "}
              {Math.floor(flightDetails.duration / 60)} hours{" "}
              {flightDetails.duration % 60} minutes
            </div>
            <div className="border-b pb-2">
              <h1 className="pb-2 text-xl font-semibold">Source</h1>
              <span className="font-semibold">Airport:</span>{" "}
              {flightDetails.source_airport}
              <div>
                <span className="font-semibold">Country:</span>{" "}
                {countries.getName(flightDetails.source_country, "en")}
              </div>
              <div>
                <span className="font-semibold">City:</span>{" "}
                {flightDetails.source_city}
              </div>
            </div>
            <div className="border-b pb-2">
              <h1 className="pb-2 text-xl font-semibold">Destination</h1>
              <span className="font-semibold">Airport:</span>{" "}
              {flightDetails.destination_airport}
              <div>
                <span className="font-semibold">Country:</span>{" "}
                {countries.getName(flightDetails.destination_country, "en")}
              </div>
              <div>
                <span className="font-semibold">City:</span>{" "}
                {flightDetails.destination_city}
              </div>
            </div>
            <div className="pb-2">
              <span className="font-semibold">Aircraft Type:</span>{" "}
              {flightDetails.aircraft_type}
            </div>
            <div className="pb-2">
              <span className="font-semibold">Status:</span>{" "}
              {flightDetails.status.charAt(0).toUpperCase() +
                flightDetails.status.slice(1)}
            </div>
          </div>
          <div className="flex flex-col lg:col-span-1">
            <span className="font-semibold">Flight Menu:</span>
            <ul className="ml-4 mt-2 list-disc">
              {flightDetails.flight_menu.map((item: string, index: number) => (
                <li className="pb-1" key={index}>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="flex justify-center gap-4 p-3">
        <div
          className="inline-flex cursor-pointer items-center justify-center rounded-full bg-primary px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={() => setView("tabular")}
        >
          Tabular View
        </div>
        <div
          className="mr-50 inline-flex cursor-pointer items-center justify-center rounded-full bg-primary px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={() => setView("extended")}
        >
          Extended View
        </div>
        <div
          className="inline-flex cursor-pointer items-center justify-center rounded-full bg-meta-3 px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={handleDownloadJSON}
        >
          Download Data JSON
        </div>
        <div
          className="inline-flex cursor-pointer items-center justify-center rounded-full bg-meta-3 px-10 py-4 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10"
          onClick={handleDownloadSQL}
        >
          Download Data SQL
        </div>
      </div>
      <div className="flex justify-center bg-slate-50 pt-4">
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
          {flightDetails.aircraft_type === "Boeing 777" ? (
            <BigSeatMap passengers={passengersPlane} />
          ) : (
            <SeatMap passengers={passengersPlane} />
          )}
        </div>
      </div>
    </DefaultLayout>
  );
};

export default FlightDetailsPage;
