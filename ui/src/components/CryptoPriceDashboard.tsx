import { useState } from 'react';

const CryptoPriceDashboard = () => {
  const [activeTab, setActiveTab] = useState('top');
  const [selectedAsset, setSelectedAsset] = useState('BTC');

  const venues = [
    { name: 'Binance', quantity: 1.28960000, bestBid: 3853.20, lastPrice: 3853.20, bestOffer: 3853.21, offerQuantity: 0.33 },
    { name: 'Deribit', quantity: 1.28960000, bestBid: 3853.20, lastPrice: 3853.20, bestOffer: 3853.21, offerQuantity: 0.33 },
    { name: 'OKX', quantity: 1.28960000, bestBid: 3853.20, lastPrice: 3853.20, bestOffer: 3853.21, offerQuantity: 0.33 },
  ];

  return (
    <div className="w-full max-w-3xl bg-gray-900 text-white p-6 rounded-lg shadow-lg ">
      <h2 className="text-2xl font-bold mb-4">Real-Time Prices</h2>
      <div className="mb-4">
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
              onChange={(e) => setSelectedAsset(e.target.value)}
            >
              <option value="BTC">BTC</option>
              <option value="ETH">ETH</option>
              <option value="LTC">LTC</option>
            </select>
          </div>
          <table className="w-full">
            <thead>
              <tr className="text-left border-b border-gray-700">
                <th className="pb-2">Venue</th>
                <th className="pb-2">Best Bid</th>
                <th className="pb-2">Last Price</th>
                <th className="pb-2">Best Offer</th>
              </tr>
              <tr className="text-sm text-gray-400">
                <th></th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Price</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {venues.map((venue, index) => (
                <tr key={index} className="border-b border-gray-800">
                  <td className="py-2">{venue.name}</td>
                  <td className="py-2">{venue.quantity.toFixed(8)}</td>
                  <td className="py-2 text-green-500">${venue.bestBid.toFixed(2)}</td>
                  <td className="py-2">${venue.lastPrice.toFixed(2)}</td>
                  <td className="py-2 text-red-500">${venue.bestOffer.toFixed(2)}</td>
                  <td className="py-2">{venue.offerQuantity.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
};

export default CryptoPriceDashboard;