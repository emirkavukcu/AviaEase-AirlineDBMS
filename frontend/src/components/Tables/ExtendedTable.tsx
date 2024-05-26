interface Pilot {
  id: number;
  person_type: string;
  name: string;
  age: number;
  gender: string;
  nationality: string;
  known_languages: string[];
  vehicle_type_id: number[];
  allowed_range: number;
  scheduled_flights: number[];
}

interface Crew {
  id: number;
  person_type: string;
  name: string;
  age: number;
  gender: string;
  nationality: string;
  known_languages: string[];
  vehicle_type_id: number[];
  attendant_type: string;
  dish_recipes?: string[];
  scheduled_flights: number[];
}

interface Passenger {
  id: number;
  person_type: string;
  name: string;
  age: number;
  gender: string;
  nationality: string;
  parent_id?: number;
  affiliated_passenger_ids: number[];
  scheduled_flights: number[];
}

interface ExtendedTableProps {
  roster: (Pilot[] | Crew[] | Passenger[])[];
}

const ExtendedTable: React.FC<ExtendedTableProps> = ({ roster }) => {
  console.log("roster", roster);
  const pilots = roster[0];
  const crew = roster[1];
  const passengers = roster[2];

  return (
    <div>
      <div className="mb-4 rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5">
        <h4 className="mb-4 text-xl font-semibold text-black dark:text-white">
          Pilots
        </h4>

        <div className="flex flex-col text-center">
          <div className="grid grid-cols-6 rounded-sm bg-gray-2 dark:bg-meta-4">
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Id
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Name
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Type
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Age
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Gender
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Nationality
              </h5>
            </div>
          </div>

          {pilots.map((pilot, key) => (
            <div
              key={pilot.id}
              className={`grid cursor-pointer grid-cols-6 hover:bg-slate-200 dark:hover:bg-meta-4 ${
                key === roster[0].length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
            >
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{pilot.id}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{pilot.name}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {pilot.person_type}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">{pilot.age}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {pilot.gender.charAt(0).toUpperCase() + pilot.gender.slice(1)}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {pilot.nationality}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-4 rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5">
        <h4 className="mb-6 text-xl font-semibold text-black dark:text-white">
          Crew
        </h4>

        <div className="flex max-h-[calc(16*1.5rem)] flex-col overflow-auto text-center">
          <div className="grid grid-cols-6 rounded-sm bg-gray-2 dark:bg-meta-4">
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Id
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Name
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Type
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Age
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Gender
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Nationality
              </h5>
            </div>
          </div>
          {crew.map((member, key) => (
            <div
              key={member.id}
              className={`grid cursor-pointer grid-cols-6 hover:bg-slate-200 dark:hover:bg-meta-4 ${
                key === roster[1].length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
            >
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{member.id}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{member.name}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {member.person_type}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">{member.age}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {member.gender.charAt(0).toUpperCase() +
                    member.gender.slice(1)}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {member.nationality}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5">
        <h4 className="mb-6 text-xl font-semibold text-black dark:text-white">
          Passengers
        </h4>

        <div className="flex max-h-[calc(29.5*1.5rem)] flex-col overflow-auto text-center">
          <div className="grid grid-cols-6 rounded-sm bg-gray-2 dark:bg-meta-4">
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Id
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Name
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Type
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Age
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Gender
              </h5>
            </div>
            <div className="p-2.5 xl:p-5">
              <h5 className="text-center text-sm font-medium uppercase xsm:text-base">
                Nationality
              </h5>
            </div>
          </div>
          {passengers.map((passenger, key) => (
            <div
              key={passenger.id}
              className={`grid cursor-pointer grid-cols-6 hover:bg-slate-200 dark:hover:bg-meta-4 ${
                key === roster[2].length - 1
                  ? ""
                  : "border-b border-stroke dark:border-strokedark"
              }`}
            >
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{passenger.id}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className=" text-black dark:text-white">{passenger.name}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {passenger.person_type}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">{passenger.age}</p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {passenger.gender.charAt(0).toUpperCase() +
                    passenger.gender.slice(1)}
                </p>
              </div>
              <div className="flex items-center justify-center p-2.5">
                <p className="text-black dark:text-white">
                  {passenger.nationality}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ExtendedTable;
