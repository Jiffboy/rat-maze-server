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
      <button className="dp-button" disabled={!data.game.directions.up || !data.game.can_vote} onClick={() => handleClick('up')}>
        <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
          <path d="M12 4l-8 8h5v8h6v-8h5z"/>
        </svg>
      </button>
      <div className="empty" />

      <button className="dp-button" disabled={!data.game.directions.left || !data.game.can_vote} onClick={() => handleClick('left')}>
        <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
          <path d="M4 12l8-8v5h8v6h-8v5z"/>
        </svg>
      </button>
      <img className="empty" src={image}/>
      <button className="dp-button" disabled={!data.game.directions.right || !data.game.can_vote} onClick={() => handleClick('right')}>
        <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
          <path d="M20 12l-8 8v-5H4V9h8V4z"/>
        </svg>
      </button>

      <div className="empty" />
      <button className="dp-button" disabled={!data.game.directions.down || !data.game.can_vote} onClick={() => handleClick('down')}>
        <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
          <path d="M12 20l8-8h-5V4H9v8H4z"/>
        </svg>
      </button>
      <div className="empty" />
    </div>
  );
};