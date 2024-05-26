"use client";
import React, { useEffect, useState } from "react";
import DefaultLayout from "@/components/Layouts/DefaultLayout";
import Select from "react-select";
import AlertError from "@/components/Alerts/AlertError";
import AlertOk from "@/components/Alerts/AlertOk";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

const hourOptions: any = [];
for (let hour = 0; hour <= 23; hour++) {
  for (let minute = 0; minute < 60; minute += 30) {
    const formattedHour = hour.toString().padStart(2, "0");
    const formattedMinute = minute.toString().padStart(2, "0");
    const label = `${formattedHour}:${formattedMinute}`;
    hourOptions.push({ value: label, label });
  }
}

const FlightCreationForm = () => {
  const [date, setDate] = useState<any>("");
  const [hour, setHour] = useState<any>("");
  const [destinationAirport, setDestinationAirport] = useState<any>("");
  const [sourceAirport, setSourceAirport] = useState<any>("");
  const [aircraftType, setAircraftType] = useState<any>("");

  const [airports, setAirports] = useState<any[]>([]);

  const [selectedCountrySource, setSelectedCountrySource] = useState<any>(null);
  const [selectedCitySource, setSelectedCitySource] = useState<any>(null);
  const [citiesSource, setCitiesSource] = useState<any[]>([]);
  const [airportOptionsSource, setAirportOptionsSource] = useState<any[]>([]);

  const [selectedCountryDestination, setSelectedCountryDestination] =
    useState<any>(null);
  const [selectedCityDestination, setSelectedCityDestination] =
    useState<any>(null);
  const [citiesDestination, setCitiesDestination] = useState<any[]>([]);
  const [airportOptionsDestination, setAirportOptionsDestination] = useState<
    any[]
  >([]);

  const [alerts, setAlerts] = useState<any[]>([]);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    const fetchAirports = async () => {
      try {
        const response = await fetchWithAuth(
          "http://127.0.0.1:5000/api/airports",
        );
        const data = await response.json();
        console.log(data);
        setAirports(data);
      } catch (error) {
        console.error("Failed to fetch airports", error);
      }
    };

    fetchAirports();
  }, []);

  useEffect(() => {
    if (selectedCountrySource) {
      const countryCities = airports
        .filter(
          (airport) =>
            airport.country === selectedCountrySource && airport.city,
        )
        .map((airport) => airport.city)
        .sort();
      setCitiesSource([...new Set(countryCities)]);
    }
  }, [selectedCountrySource]);

  useEffect(() => {
    if (selectedCitySource) {
      const cityAirports = airports
        .filter(
          (airport) => airport.city === selectedCitySource && airport.city,
        )
        .map((airport) => airport.airport_code);
      setAirportOptionsSource(cityAirports);
    }
  }, [selectedCitySource]);

  useEffect(() => {
    if (selectedCountryDestination) {
      const countryCities = airports
        .filter((airport) => airport.country === selectedCountryDestination)
        .map((airport) => airport.city)
        .sort();
      setCitiesDestination([...new Set(countryCities)]);
    }
  }, [selectedCountryDestination]);

  useEffect(() => {
    if (selectedCityDestination) {
      const cityAirports = airports
        .filter((airport) => airport.city === selectedCityDestination)
        .map((airport) => airport.airport_code);
      setAirportOptionsDestination(cityAirports);
    }
  }, [selectedCityDestination]);

  const getAircraftTypeId = (aircraftType: string) => {
    switch (aircraftType) {
      case "Airbus A320":
        return 2;
      case "Boeing 737":
        return 1;
      case "Boeing 777":
        return 3;
      default:
        return null;
    }
  };

  const addAlert = (type: "error" | "success", message: string) => {
    const id = Date.now();
    setAlerts((prevAlerts) => [...prevAlerts, { id, type, message }]);
    setTimeout(() => {
      setAlerts((prevAlerts) => prevAlerts.filter((alert) => alert.id !== id));
    }, 3000);
  };

  const createFlight = async () => {
    if (date && hour && destinationAirport && sourceAirport && aircraftType) {
      setIsCreating(true);
      const flight_time = `${date}T${hour.value}:00`;
      const source = sourceAirport;
      const destination = destinationAirport;
      const vehicle_type_id = getAircraftTypeId(aircraftType);

      console.log(flight_time, source, destination, vehicle_type_id);

      const response = await fetchWithAuth(
        "http://127.0.0.1:5000/api/create_flight",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            flight_time,
            source,
            destination,
            vehicle_type_id,
            create_roster: "Yes",
          }),
        },
      );

      setIsCreating(false);

      if (response.ok) {
        setDate("");
        setHour(null);
        setDestinationAirport(null);
        setSourceAirport(null);
        setAircraftType(null);
        setSelectedCountrySource(null);
        setSelectedCitySource(null);
        setSelectedCountryDestination(null);
        setSelectedCityDestination(null);
        addAlert("success", "Flight successfully created");
      } else {
        addAlert("error", "Failed to create flight");
      }
    } else {
      addAlert("error", "All fields must be filled");
    }
  };

  const uniqueCountryOptions = Array.from(
    new Set(airports.map((airport) => airport.country)),
  )
    .sort()
    .map((country) => ({ value: country, label: country }));

  return (
    <DefaultLayout>
      <div className="flex justify-center">
        <div className="flex w-1/2 flex-col">
          <div className="grayinputs rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
            <div className="border-b border-stroke px-10 py-4 dark:border-strokedark">
              <h3 className="text-2xl font-medium text-black dark:text-white">
                Flight Creation
              </h3>
            </div>
            <div className="flex flex-col gap-3 p-10 text-lg">
              <div className="flex gap-4">
                <div className="mb-4.5">
                  <label className="mb-3 block font-medium text-black dark:text-white">
                    Date
                  </label>
                  <input
                    type="date"
                    className="rounded-sm border border-graydark bg-white p-1  dark:border-strokedark dark:bg-boxdark"
                    onChange={(e) => setDate(e.target.value)}
                    value={date}
                  />
                </div>

                <div className="mb-4.5 w-full">
                  <label className="mb-3 block w-full font-medium text-black dark:text-white">
                    Hour
                  </label>
                  <Select
                    options={hourOptions}
                    placeholder="Select Hour"
                    onChange={setHour}
                    value={hour}
                  />
                </div>
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Source Country
                </label>
                <Select
                  options={uniqueCountryOptions}
                  placeholder="Select Source Country"
                  onChange={(selectedOption) =>
                    setSelectedCountrySource(selectedOption?.value)
                  }
                  value={uniqueCountryOptions.find(
                    (country) => country.value === selectedCountrySource,
                  )}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Source City
                </label>
                <Select
                  options={citiesSource.map((city) => ({
                    value: city,
                    label: city,
                  }))}
                  placeholder="Select Source City"
                  onChange={(selectedOption) =>
                    setSelectedCitySource(selectedOption?.value)
                  }
                  isDisabled={!selectedCountrySource}
                  value={
                    selectedCitySource
                      ? { value: selectedCitySource, label: selectedCitySource }
                      : null
                  }
                />
              </div>

              <div className="mb-4.5">
                <label className="tfont-medium mb-3 block text-black dark:text-white">
                  Source Airport
                </label>
                <Select
                  options={airportOptionsSource.map((airport) => ({
                    value: airport,
                    label: airport,
                  }))}
                  placeholder="Select Source Airport"
                  onChange={(selectedOption) =>
                    setSourceAirport(selectedOption?.value)
                  }
                  isDisabled={!selectedCitySource}
                  value={
                    sourceAirport
                      ? { value: sourceAirport, label: sourceAirport }
                      : null
                  }
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Destination Country
                </label>
                <Select
                  options={uniqueCountryOptions}
                  placeholder="Select Destination Country"
                  onChange={(selectedOption) =>
                    setSelectedCountryDestination(selectedOption?.value)
                  }
                  value={uniqueCountryOptions.find(
                    (country) => country.value === selectedCountryDestination,
                  )}
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Destination City
                </label>
                <Select
                  options={citiesDestination.map((city) => ({
                    value: city,
                    label: city,
                  }))}
                  placeholder="Select Destination City"
                  onChange={(selectedOption) =>
                    setSelectedCityDestination(selectedOption?.value)
                  }
                  isDisabled={!selectedCountryDestination}
                  value={
                    selectedCityDestination
                      ? {
                          value: selectedCityDestination,
                          label: selectedCityDestination,
                        }
                      : null
                  }
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Destination Airport
                </label>
                <Select
                  options={airportOptionsDestination.map((airport) => ({
                    value: airport,
                    label: airport,
                  }))}
                  placeholder="Select Destination Airport"
                  onChange={(selectedOption) =>
                    setDestinationAirport(selectedOption?.value)
                  }
                  isDisabled={!selectedCityDestination}
                  value={
                    destinationAirport
                      ? { value: destinationAirport, label: destinationAirport }
                      : null
                  }
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-3 block font-medium text-black dark:text-white">
                  Aircraft Type
                </label>
                <Select
                  options={[
                    { value: "Airbus A320", label: "Airbus A320" },
                    { value: "Boeing 737", label: "Boeing 737" },
                    { value: "Boeing 777", label: "Boeing 777" },
                  ]}
                  placeholder="Select Aircraft Type"
                  onChange={(selectedOption) =>
                    setAircraftType(selectedOption?.value)
                  }
                  value={
                    aircraftType
                      ? { value: aircraftType, label: aircraftType }
                      : null
                  }
                />
              </div>

              <button
                className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90 disabled:opacity-50"
                onClick={createFlight}
                disabled={isCreating}
              >
                {isCreating ? "Creating..." : "Create Flight"}
              </button>

              <div className="fixed bottom-5 right-5 space-y-2">
                {alerts.map((alert) =>
                  alert.type === "error" ? (
                    <div
                      key={alert.id}
                      className="w-100 opacity-100 transition-opacity duration-1000 ease-out"
                    >
                      <AlertError message={alert.message} />
                    </div>
                  ) : (
                    <div
                      key={alert.id}
                      className="w-100 opacity-100 transition-opacity duration-1000 ease-out"
                    >
                      <AlertOk message={alert.message} />
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};

export default FlightCreationForm;
