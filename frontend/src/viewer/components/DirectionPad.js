import React, { useState, useEffect } from 'react';
import './DirectionPad.css';
import image from '../../assets/rat.png';

export default function DirectionPad({data, socket}) {
  const handleClick = (direction) => {
    socket.current.emit("vote", { direction: direction})
  };

  return (
    <div className="direction-pad">
      <div className="empty" />
      <button className="dp-button" disabled={!data.game.directions.up || !data.game.can_vote} onClick={() => handleClick('up')}>↑</button>
      <div className="empty" />

      <button className="dp-button" disabled={!data.game.directions.left || !data.game.can_vote} onClick={() => handleClick('left')}>←</button>
      <img className="empty" src={image}/>
      <button className="dp-button" disabled={!data.game.directions.right || !data.game.can_vote} onClick={() => handleClick('right')}>→</button>

      <div className="empty" />
      <button className="dp-button" disabled={!data.game.directions.down || !data.game.can_vote} onClick={() => handleClick('down')}>↓</button>
      <div className="empty" />
    </div>
  );
};