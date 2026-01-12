import React, { useEffect, useState, useRef } from "react";
import DirectionPad from './DirectionPad'
import Item from './Item'
import './App.css'
import loadingImg from './assets/loading.gif';
import { io } from 'socket.io-client'

export default function UserDataPanel() {
  const [userId, setUserId] = useState(null);
  const [data, setData] = useState(null);
  const socket = useRef(null)

  useEffect(() => {
    if (window.Twitch && window.Twitch.ext) {
      window.Twitch.ext.onAuthorized((auth) => {
        if (auth?.userId) {
          setUserId(auth.userId.slice(1));
          socket.current = io( "/ratmaze/widget", {
            auth: { id: auth.userId.slice(1) }
          });

          socket.current.on("data_update", (payload) => {
            setData(payload)
            console.log(payload)
          })
        }
      });
    }
  }, []);

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
  console.log(data)
  return (
    <div>
      <div className="point-bar">
        <p><strong>Current:</strong> {data.user.current_points}</p>
        <p className="point-right"><strong>All-Time:</strong> {data.user.total_points}</p>
      </div>
      <p>{data.game.turn_start}</p>
      <DirectionPad
        data={data}
        socket={socket}
      />
      <hr/>
      <p><strong>Balance:</strong> {data.user.balance}</p>

      {data.game.shop.map((item, index) => (
        <Item data={item} balance={data.user.balance} socket={socket}/>
      ))}
    </div>
  );
}