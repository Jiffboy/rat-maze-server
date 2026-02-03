import React, { useState, useEffect } from 'react';

export default function DebugBar({socket}) {
  const givePoints = () => {
    socket.current.emit("give_points")
  };

  const resetShop = () => {
    socket.current.emit("refresh_shop")
  }

  return (
    <div>
      <button onClick={() => givePoints()}>Give points</button>
      <button onClick={() => resetShop()}>Reset shop</button>
    </div>
  );
};