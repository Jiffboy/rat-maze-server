import React, { useState, useEffect } from 'react';
import './DirectionPad.css';
import image from './rat.png';

export default function DirectionPad({data}) {
  const [disableOverride, setDisableOverride] = useState(false)
  const [nextTurn, setNextTurn] = useState(0)


  const handleClick = (direction) => {
      fetch(`/ratmaze/vote?id=${data.user.id}&direction=${direction}`, {
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            setDisableOverride(true)
          })
          .catch((err) => console.error("Error:", err));
          };

  useEffect(() => {
    if (data.game.next_turn > nextTurn) {
        setNextTurn(data.game.next_turn)
        setDisableOverride(false)
    }
  }, [data])

  return (
    <div className="direction-pad">
      <div className="empty" />
      <button className="dp-button" disabled={!data.game.directions.up || disableOverride} onClick={() => handleClick('up')}>↑</button>
      <div className="empty" />

      <button className="dp-button" disabled={!data.game.directions.left || disableOverride} onClick={() => handleClick('left')}>←</button>
      <img className="empty" src={image}/>
      <button className="dp-button" disabled={!data.game.directions.right || disableOverride} onClick={() => handleClick('right')}>→</button>

      <div className="empty" />
      <button className="dp-button" disabled={!data.game.directions.down || disableOverride} onClick={() => handleClick('down')}>↓</button>
      <div className="empty" />
    </div>
  );
};