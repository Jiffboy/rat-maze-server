import React, { useState, useEffect } from 'react';
import './Item.css';

export default function DirectionPad({data, balance, user_id}) {
    const handleClick = (direction) => {
      fetch(`/ratmaze/buy?id=${user_id}&item=${data.id}`, {
          method: "POST",
        })
          .then(/*handle whatever*/)
          .catch((err) => console.error("Error:", err));
  };

  const getRarityType = (rarity) => {
    return 'rarity-' + rarity.toLowerCase()
  }
  return (
    <div className={'item-container'}>
    <button className={`item-button ${getRarityType(data.rarity)}`}
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