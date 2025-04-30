import React from "react";
import { Image, View, Text, StyleSheet } from 'react-native';
import "@/components/EventCard.css"

const imageAssets = {
    event1: require('@/assets/images/image1.png'),
    event2: require('@/assets/images/image2.png')
};

function EventCard({ event }) {
  return (
    <div className="event">
        <Image source={imageAssets[event.image]} accessibilityLabel={event.title} className="event-img"/>
      <div className="event-info">
        <h3>{event.title}</h3>
        <div className="event-details">
          <span>{event.date}</span> • <span>{event.location}</span>
        </div>
        <div className="event-organization">{event.organization}</div>
        <div className="event-tags">
          {event.tags.map(tag => (
           <span className="tag"> {tag} </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default EventCard;
