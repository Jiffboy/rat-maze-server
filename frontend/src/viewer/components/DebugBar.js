import React, { useState, useEffect } from 'react';

export default function DebugBar({socket}) {
  const [id, setId] = useState('');
  const givePoints = () => {
    socket.current.emit("give_points")
  };

  const resetShop = () => {
    socket.current.emit("refresh_shop")
  }

  const vote = (direction) => {
    socket.current.emit("vote_as", {id: id, direction: direction})
  }

  const handleChange = (event) => {
    setId(event.target.value)
  }

  return (
    <div>
      <button onClick={() => givePoints()}>Give points</button>
      <button onClick={() => resetShop()}>Reset shop</button>
      <button onClick={() => vote("right")}>Right</button>
      <button onClick={() => vote("up")}>Up</button>
      <button onClick={() => vote("down")}>Down</button>
      <button onClick={() => vote("left")}>Left</button>
      <input type="text" value={id} onChange={handleChange}/>
    </div>
  );
};