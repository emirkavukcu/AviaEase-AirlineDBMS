"use client";
import React, { useState, useRef } from "react";

interface Passenger {
  id: number;
  name: string;
  person_type: string;
  seat_number: string;
  seat_row: string;
  seat_type: string;
  seniority_level?: string;
  affiliated_passenger_ids?: number[];
  parent_id?: number;
}

interface BigSeatMapProps {
  passengers: Passenger[];
}

const BigSeatMap: React.FC<BigSeatMapProps> = ({ passengers = [] }) => {
  const [hoveredPassenger, setHoveredPassenger] = useState<Passenger | null>(
    null,
  );
  const [hoverPosition, setHoverPosition] = useState<{
    x: number;
    y: number;
  } | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseMove = (event: React.MouseEvent) => {
    if (containerRef.current) {
      const containerRect = containerRef.current.getBoundingClientRect();
      const xOffset = 10; // Distance from the cursor
      const yOffset = 10; // Distance from the cursor
      const cursorX = event.clientX - containerRect.left;
      const cursorY = event.clientY - containerRect.top;

      setHoverPosition({ x: cursorX + xOffset, y: cursorY + yOffset });
    }
  };

  const handleMouseEnter = (passenger: Passenger) => {
    setHoveredPassenger(passenger);
  };

  const handleMouseLeave = () => {
    setHoveredPassenger(null);
    setHoverPosition(null);
  };

  const renderSeats = (
    numRows: number,
    seatsPerRow: number,
    rowStartLetter: string,
    filledSeats: number[],
    showLetters: boolean,
    businessClass: boolean = false,
    pilotRow: boolean = false,
    crewRow: boolean = false,
  ) => {
    const rows = [];
    let rowLetter = rowStartLetter.charCodeAt(0);

    for (let i = 0; i < numRows; i++) {
      const row = [];
      let seatNumber = 1;

      for (let j = 1; j <= seatsPerRow; j++) {
        const seatRowLabel = String.fromCharCode(rowLetter);
        let passenger: Passenger | undefined;

        if (pilotRow) {
          passenger = passengers.find(
            (p) =>
              p.seat_row === "PL" && parseInt(p.seat_number) === seatNumber,
          );
        } else if (crewRow) {
          passenger = passengers.find(
            (p) =>
              p.seat_row === "CR" && parseInt(p.seat_number) === seatNumber,
          );
        } else {
          passenger = passengers.find(
            (p) =>
              p.seat_row === seatRowLabel &&
              parseInt(p.seat_number) === seatNumber,
          );
        }

        if (filledSeats.includes(j)) {
          row.push(
            <div
              className={`bg-gray-400 seat-shape m-1 flex h-8 w-8 items-center justify-center rounded text-black ${passenger ? "seat-filled cursor-pointer" : ""}`}
              key={`${seatRowLabel}-${seatNumber}`}
              onMouseEnter={() => passenger && handleMouseEnter(passenger)}
              onMouseLeave={handleMouseLeave}
              onMouseMove={handleMouseMove}
            >
              {seatNumber}
            </div>,
          );
          seatNumber++;
        } else {
          row.push(<div className="m-1 h-8 w-8" key={`empty-${i}-${j}`}></div>);
        }
      }
      rows.push(
        <div
          className="mb-2 flex items-center justify-center"
          key={String.fromCharCode(rowLetter)}
        >
          {showLetters && (
            <span className="font-mono mr-2 w-10 text-center">
              {pilotRow
                ? `PL`
                : crewRow
                  ? `CR`
                  : String.fromCharCode(rowLetter)}
            </span>
          )}
          {row}
        </div>,
      );
      rowLetter++;
    }

    return <div className="mb-4">{rows}</div>;
  };

  return (
    <div
      className="airplane-container-big relative flex flex-col items-center p-4"
      ref={containerRef}
    >
      {/* Pilot Seats */}
      <div className="mb-4">
        {renderSeats(1, 7, "A", [1, 2, 3, 5, 6, 7], true, false, true, false)}
      </div>

      {/* Crew Members Seats */}
      <div className="mb-4">
        {renderSeats(
          2,
          10,
          "A",
          [1, 2, 3, 5, 6, 8, 9, 10],
          true,
          false,
          false,
          true,
        )}
      </div>

      {/* Business Passengers Seats */}
      <div className="mb-4">
        {renderSeats(10, 7, "A", [1, 3, 5, 7], true, true, false, false)}
      </div>

      {/* Economy Passengers Seats */}
      <div className="mb-4">
        {renderSeats(
          15,
          10,
          "A",
          [1, 2, 3, 5, 6, 8, 9, 10],
          true,
          false,
          false,
          false,
        )}
      </div>

      {hoveredPassenger && hoverPosition && (
        <div
          className="border-gray-300 absolute rounded border bg-white p-4 shadow-lg"
          style={{
            top: `${hoverPosition.y}px`,
            left: `${hoverPosition.x}px`,
            whiteSpace: "nowrap",
            overflow: "hidden",
          }}
        >
          <h3 className="text-lg font-bold">{hoveredPassenger.name}</h3>
          <p>{hoveredPassenger.person_type}</p>
          <p>
            Seat: {hoveredPassenger.seat_row}
            {hoveredPassenger.seat_number}
          </p>
        </div>
      )}
    </div>
  );
};

export default BigSeatMap;
