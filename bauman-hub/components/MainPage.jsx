import React from "react";
import EventCard from "@/components/EventCard.jsx";
import EventsData from "@/components/news.json";
import "@/components/EventCard.css";
import "@/components/MainPage.css";

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