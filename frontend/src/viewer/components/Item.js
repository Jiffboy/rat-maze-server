import React, { useState, useEffect } from 'react';
import './Item.css';

export default function DirectionPad({data, balance, socket}) {
    const handleClick = (direction) => {
      socket.current.emit("buy", { item: data.id})
  };

  const getRarityType = (rarity) => {
    return 'rarity-' + rarity.toLowerCase()
  }
  return (
    <div className={'item-container'}>
    <button className={`item-button ${getRarityType(data.rarity)}`}
            title={data.description}
            disabled={balance < data.cost || (data.total_stock > 0 && data.current_stock <=0)}
            onClick={() => handleClick()}>
      <p>{data.name}</p>
      {data.total_stock > 0 &&
        <p>{data.current_stock}/{data.total_stock}</p>
      }
      <p className='item-cost'>{data.cost}</p>
    </button>
    </div>
  );
};