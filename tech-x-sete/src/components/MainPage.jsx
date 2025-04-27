import React from "react";
import EventCard from "./EventCard.jsx";
import EventsData from "../news.json";
import "../EventCard.css";
import "../MainPage.css";

function MainPage() {
    return (
    <div className="container">
        <h2>События в университете</h2>
        <input type="text" placeholder="Название, тег или организатор" className="search-input"/>
        {EventsData.map(eventData => (
            <EventCard 
                key={eventData.id}
                event={eventData} 
            />
            ))}
    </div>
    );
  }

export default MainPage;