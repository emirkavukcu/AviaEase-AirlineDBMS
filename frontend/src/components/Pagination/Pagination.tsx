"use client";
import React from "react";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationProps) => {
  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      onPageChange(page);
    }
  };

  return (
    <div className="mt-4 flex justify-center">
      <button
        className="mx-1 rounded border px-4 py-2"
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
      >
        Previous
      </button>
      {[...Array(totalPages)].map((_, index) => (
        <button
          key={index}
          className={`mx-1 rounded border px-4 py-2 ${currentPage === index + 1 ? "bg-blue-500 text-white" : ""}`}
          onClick={() => handlePageChange(currentPage + 1)}
        >
          {index + 1}
        </button>
      ))}
      <button
        className="mx-1 rounded border px-4 py-2"
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
