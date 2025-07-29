import React from 'react';

const PlusIcon = ({ className }: { className?: string }) => {
  return (
    <svg
      fill="currentColor"
      viewBox="0 0 500 500" // The coordinate system is 500x500
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* This new path data draws a plus sign in the exact center of the 500x500 viewBox */}
      <path d="M275,100 v125 h125 v50 h-125 v125 h-50 v-125 h-125 v-50 h125 v-125 Z" />
    </svg>
  );
};

export default PlusIcon;