
import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-1 text-health-600">
      <div 
        className="w-2 h-2 bg-health-500 rounded-full animate-pulse-dot"
        style={{ animationDelay: '0ms' }}
      ></div>
      <div 
        className="w-2 h-2 bg-health-500 rounded-full animate-pulse-dot"
        style={{ animationDelay: '160ms' }}
      ></div>
      <div 
        className="w-2 h-2 bg-health-500 rounded-full animate-pulse-dot"
        style={{ animationDelay: '320ms' }}
      ></div>
    </div>
  );
};

export default TypingIndicator;
