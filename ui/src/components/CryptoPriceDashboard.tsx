import { useState, useEffect, useRef } from 'react';

const SYMBOLS = import.meta.env.VITE_SYMBOLS.split(',');
const WEBSOCKET_URL = import.meta.env.VITE_WEBSOCKET_URL

const VENUES = import.meta.env.VITE_EXCHANGES.split(',');

// Define the type for venue data
interface VenueData {
  best_bid_quantity?: number;
  best_bid_price?: number;
  last_price?: number;
  best_offer_price?: number;
  best_offer_quantity?: number;
}

const CryptoPriceDashboard = () => {
  const [activeTab, setActiveTab] = useState('top');
  const [selectedAsset, setSelectedAsset] = useState(SYMBOLS[0]);
  const [venueData, setVenueData] = useState<Record<string, VenueData>>({});
  const websockets = useRef<Record<string, WebSocket>>({}); // Explicitly type websockets

  useEffect(() => {
    // Close all existing WebSocket connections
    Object.values(websockets.current).forEach(ws => ws.close());
    websockets.current = {};

    // Create new WebSocket connections for each venue
    VENUES.forEach(venue => {
      const ws = new WebSocket(`${WEBSOCKET_URL}/${venue.toLowerCase()}/${selectedAsset.toLowerCase()}`);
      
      ws.onopen = () => {
        console.log(`Connected to ${venue} for ${selectedAsset}`);
        ws.send(JSON.stringify({ action: 'subscribe', ticker: selectedAsset }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setVenueData(prevData => ({
          ...prevData,
          [venue]: data
        }));
      };

      ws.onerror = (error) => {
        console.error(`WebSocket error for ${venue}:`, error);
      };

      ws.onclose = () => {
        console.log(`Disconnected from ${venue} for ${selectedAsset}`);
      };

      websockets.current[venue] = ws; // Store the WebSocket connection in websockets
    });

    // Cleanup function to close WebSockets when component unmounts or selectedAsset changes
    return () => {
      Object.values(websockets.current).forEach(ws => ws.close());
    };
  }, [selectedAsset]);

  const handleAssetChange = (newAsset: string) => {
    setSelectedAsset(newAsset);
  };

  return (
    <div className="w-full max-w-4xl bg-gray-900 text-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4 text-center">Real-Time Prices</h2>
      <div className="mb-4 flex justify-center">
        <button
          className={`px-4 py-2 rounded-md mr-2 ${activeTab === 'top' ? 'bg-blue-600' : 'bg-gray-700'}`}
          onClick={() => setActiveTab('top')}
        >
          Top of Books
        </button>
        <button
          className={`px-4 py-2 rounded-md ${activeTab === 'full' ? 'bg-blue-600' : 'bg-gray-700'}`}
          onClick={() => setActiveTab('full')}
        >
          Full Books
        </button>
      </div>
      {activeTab === 'top' && (
        <>
          <div className="mb-4">
            <select
              className="w-full bg-gray-800 text-white p-2 rounded"
              value={selectedAsset}
              onChange={(e) => handleAssetChange(e.target.value)}
            >
              {
                SYMBOLS.map((symbol) =>{
                  return <option value={symbol}>{symbol}</option>
                })
              }
              
            </select>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b border-gray-700">
                  <th className="pb-2">Venue</th>
                  <th colSpan={2} className="pb-2 pl-20">Best Bid</th>
                  <th className="pb-2">Last Price</th>
                  <th colSpan={2} className="pb-2 pl-16">Best Offer</th>
                </tr>
                <tr className="text-sm text-gray-400">
                  <th className="w-1/6 text-left"></th>
                  <th className="w-1/6 text-left">Quantity</th>
                  <th className="w-1/6 text-left">Price</th>
                  <th className="w-1/6 text-left"></th>
                  <th className="w-1/6 text-left">Price</th>
                  <th className="w-1/6 text-left">Quantity</th>
                </tr>
              </thead>
              <tbody>
                {VENUES.map((venue) => {
                  const data = venueData[venue] || {};
                  return (
                    <tr key={venue} className="border-b border-gray-800">
                      <td className="py-2">{venue}</td>
                      <td className="py-2">{data.best_bid_quantity || '-'}</td>
                      <td className="py-2 text-green-500">{data.best_bid_price ? 
                                                            new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.best_bid_price) : 
                                                            '-'}</td>
                      <td className="py-2">{data.last_price ? 
                                                            new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.last_price) : 
                                                            '-'}</td>
                      <td className="py-2 text-red-500">{data.best_offer_price ? 
                                                            new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.best_offer_price) : 
                                                            '-'}</td>
                      <td className="py-2">{data.best_offer_quantity || '-'}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};

export default CryptoPriceDashboard;
