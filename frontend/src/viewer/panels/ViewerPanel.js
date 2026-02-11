import React, { useEffect, useState, useRef } from "react";
import OnlinePanel from './OnlinePanel'
import OfflinePanel from './OfflinePanel'
import loadingImg from '../../assets/loading.gif';
import { io } from 'socket.io-client'

export default function ViewerPanel() {
  const [data, setData] = useState(null)
  const socket = useRef(null)

  useEffect(() => {
    if (window.Twitch && window.Twitch.ext) {
      window.Twitch.ext.onAuthorized((auth) => {
        if (auth?.userId) {
          socket.current = io("https://jifbot.com/ratmaze/widget", {
            path: "/socket.io",
            transports: ["websocket", "polling"],
            auth: { id: auth.userId.slice(1) }
          });

          socket.current.on("data_update", (payload) => {
            setData(payload)
          })
        }
      });
    }
  }, []);

  return (
  <div>
    {!data &&
        <div className='loading-container'>
          <div>
            <img className='loading-img' src={loadingImg}/>
            <p>Loading...</p>
          </div>
        </div>
    }
    {data && data.game.is_live && <OnlinePanel data={data} socket={socket}/>}
    {data && !data.game.is_live && <OfflinePanel data={data} socket={socket}/>}
  </div>
  )
}