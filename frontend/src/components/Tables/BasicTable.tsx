interface Passenger {
  id: number;
  name: string;
  person_type: string;
}

interface BasicTableProps {
  passengers: Passenger[];
}

const BasicTable: React.FC<BasicTableProps> = ({ passengers = [] }) => {
  return (
    <div className="h-[calc(63.85*1.5rem)] w-150 rounded-sm border border-stroke bg-white px-5 pb-2.5 pt-6 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
      <h4 className="mb-6 text-xl font-semibold text-black dark:text-white">
        Roster
      </h4>

      <div className="flex max-h-[calc(60*1.5rem)] flex-col overflow-auto">
        <div className="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4">
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
        </div>
        {passengers.map((passenger, key) => (
          <div
            key={passenger.id}
            className={`grid cursor-pointer grid-cols-3 hover:bg-slate-200 dark:hover:bg-meta-4 ${
              key === passengers.length - 1
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
          </div>
        ))}
      </div>
    </div>
  );
};

export default BasicTable;
