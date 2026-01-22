
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default Leaflet icon not showing
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const RecenterMap = ({ lat, lon }) => {
    const map = useMap();
    useEffect(() => {
        if (lat && lon) {
            map.flyTo([lat, lon], map.getZoom());
        }
    }, [lat, lon, map]);
    return null;
}

const MapComponent = ({ lat, lon, zoom = 13, markers = [], height = '300px' }) => {
    // Default to a central location if no lat/lon provided (e.g. Ludhiana)
    const centerLat = lat || 30.9010;
    const centerLon = lon || 75.8573;

    return (
        <MapContainer center={[centerLat, centerLon]} zoom={zoom} style={{ height: height, width: '100%', borderRadius: '12px' }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <RecenterMap lat={centerLat} lon={centerLon} />

            {/* Single Marker (Main focus) */}
            {lat && lon && <Marker position={[lat, lon]} />}

            {/* Multiple Markers */}
            {markers.map((marker, idx) => (
                <Marker key={idx} position={[marker.lat, marker.lon]}>
                    <Popup>
                        {marker.popupText}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
};

export default MapComponent;
