import React, { useEffect, useState } from "react";
import DirectionPad from './DirectionPad'
import Item from './Item'
import './App.css'
import loadingImg from './assets/loading.gif';

export default function UserDataPanel() {
  const [userId, setUserId] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    if (window.Twitch && window.Twitch.ext) {
      window.Twitch.ext.onAuthorized((auth) => {
        if (auth?.userId) {
          setUserId(auth.userId.slice(1));
        }
      });
    }
  }, []);

  useEffect(() => {
    if (!userId) return;

    const fetchData = async () => {
      try {
        const res = await fetch(`/ratmaze/userdata/${userId}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setData(data.data ?? data);
      } catch (err) {
        console.error("Fetch error:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 500);

    return () => clearInterval(interval);
  }, [userId]);

  if (!data) {
    return (
      <div className='loading-container'>
          <div>
            <img className='loading-img' src={loadingImg}/>
            <p>Loading...</p>
          </div>
      </div>
    )
  }

  return (
    <div>
      <div className="point-bar">
        <p><strong>Current:</strong> {data.user.current_points}</p>
        <p className="point-right"><strong>All-Time:</strong> {data.user.total_points}</p>
      </div>
      <p>{data.game.turn_start}</p>
      <DirectionPad
        data={data}
      />
      <hr/>
      <p><strong>Balance:</strong> {data.user.balance}</p>

      {data.game.shop.map((item, index) => (
        <Item data={item} balance={data.user.balance} user_id={data.user.id}/>
      ))}
    </div>
  );
}