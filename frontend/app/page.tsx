'use client';

import React, { useState, useEffect } from 'react';
import { pokemonService, PokemonPrediction, Collection } from '../lib/pokemon-service';

export default function Home() {
  const [prediction, setPrediction] = useState<PokemonPrediction | null>(null);
  const [collection, setCollection] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [showCollection, setShowCollection] = useState(false);
  const [imageUrl, setImageUrl] = useState('');

  const handleCapture = async () => {
    setIsLoading(true);
    setCountdown(2);
    try {
      const success = await pokemonService.captureImage();
      if (success) {
        // Countdown timer
        const timer = setInterval(() => {
          setCountdown(prev => {
            if (prev <= 1) {
              clearInterval(timer);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);

        // Wait for 2 seconds before getting prediction
        await new Promise(resolve => setTimeout(resolve, 2000));
        const result = await pokemonService.predictPokemon();
        setPrediction(result);
        setImageUrl(pokemonService.getLatestImageUrl());
      }
    } catch (error) {
      console.error('Error capturing:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFavorite = async () => {
    if (prediction) {
      const success = await pokemonService.favoritePokemon(prediction.name);
      if (success) {
        const updatedCollection = await pokemonService.getCollection();
        if (updatedCollection) {
          setCollection(updatedCollection.collection);
        }
      }
    }
  };

  const handleShowCollection = async () => {
    const result = await pokemonService.getCollection();
    if (result) {
      setCollection(result.collection);
      setShowCollection(true);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-red-500 to-red-700 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white text-center mb-8">
          Raspberry Pi Pokédex
        </h1>

        <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
          <div className="aspect-video bg-gray-100 rounded-lg mb-4 overflow-hidden relative">
            {imageUrl ? (
              <img
                src={imageUrl}
                alt="Captured Pokemon"
                className="w-full h-full object-contain"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No image captured
              </div>
            )}
            {isLoading && countdown > 0 && (
              <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="text-white text-4xl font-bold">
                  Analyzing in {countdown}s...
                </div>
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 gap-4">
            <button
              onClick={handleCapture}
              disabled={isLoading}
              className="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-6 rounded-lg text-xl transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Processing...' : 'Take Picture'}
            </button>

            {prediction && (
              <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden my-6 border-2 border-red-400">
                <div className="flex flex-col items-center p-6">
                  <img
                    src={imageUrl}
                    alt={prediction.name}
                    className="w-40 h-40 object-contain mb-4 drop-shadow-lg"
                  />
                  <h2 className="text-3xl font-extrabold text-red-600 mb-2">{prediction.name}</h2>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-3 py-1 rounded-full bg-green-200 text-green-800 text-sm font-semibold">
                      {prediction.type}
                    </span>
                    <span className="flex items-center gap-1 text-gray-700 text-sm">
                      <svg className="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
                      </svg>
                      {prediction.hp} HP
                    </span>
                  </div>
                  <div className="mb-2 text-gray-700">
                    <span className="font-semibold">Evolves to:</span> {prediction.evolves_to && prediction.evolves_to !== 'None' ? (
                      <span className="ml-1 px-2 py-1 rounded bg-blue-100 text-blue-800 text-xs font-semibold">{prediction.evolves_to}</span>
                    ) : (
                      <span className="ml-1 text-gray-400">None</span>
                    )}
                  </div>
                  <div className="mb-2 w-full">
                    <span className="font-semibold text-gray-700">Attacks:</span>
                    <ul className="list-disc list-inside text-gray-600">
                      {prediction.attacks.map((attack, idx) => (
                        <li key={idx}>{attack}</li>
                      ))}
                    </ul>
                  </div>
                  <p className="italic text-gray-500 text-center mt-2">{prediction.desc}</p>
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={handleFavorite}
                disabled={!prediction}
                className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-4 px-6 rounded-lg text-xl transition-colors disabled:opacity-50"
              >
                Favorite
              </button>
              <button
                onClick={handleShowCollection}
                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-6 rounded-lg text-xl transition-colors"
              >
                Show Collection
              </button>
            </div>
          </div>
        </div>

        {showCollection && (
          <div className="bg-white rounded-lg shadow-xl p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Your Collection
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
              {collection.map((pokemon, index) => (
                <div
                  key={index}
                  className="bg-gray-50 p-3 rounded-lg text-center"
                >
                  {pokemon}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 