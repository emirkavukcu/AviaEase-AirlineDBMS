import React from "react";
import Calendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";

const CalendarComponent: React.FC = () => {
  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-7">
      <h4 className="mb-2 text-xl font-semibold text-black dark:text-white">
        Calendar
      </h4>
      <div className="h-1000"> {}
        <Calendar
          plugins={[dayGridPlugin]}
          initialView="dayGridMonth"
          fixedWeekCount={false}
          height={450}
          events={[]}
        />
      </div>
    </div>
  );
};

export default CalendarComponent;
