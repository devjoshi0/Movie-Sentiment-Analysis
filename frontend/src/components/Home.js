import React, {useState, useEffect} from 'react';
import axios from 'axios';
import MovieCard from './MovieCard';
import './Home.css';

const Home = () => {
    const [trending, setTrending] = useState([]);
    const [popularMovies, setPopularMovies] = useState([]);
    const [popularTv, setPopularTv] = useState([]);
    const [newReleases, setNewReleases] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const trendingResponse = await axios.get('HTTP://localhost:5173/');
            const popularMoviesResponse = await axios.get('http://localhost:5173/popular_movies');
            const popularTvResponse = await axios.get('http://localhost:5173/popular_tv');
            const newReleasesResponse = await axios.get('http://localhost:5173/new_releases');

            setTrending(trendingResponse.data.trending);
            setPopularMovies(popularMoviesResponse.data);
            setPopularTv(popularTvResponse.data);
            setNewReleases(newReleasesResponse.data);
    };
    fetchData();
}, []);

    return (
        <div className="home">
            <h1>Trending</h1>
            <div className="movie-container">
                {trending.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                ))}
            </div>
            <h1>Popular Movies</h1>
            <div className="movie-container">
                {popularMovies.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                ))}
            </div>
            <h1>Popular TV Shows</h1>
            <div className="movie-container">
                {popularTv.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                ))}
            </div>
            <h1>New Releases</h1>
            <div className="movie-container">
                {newReleases.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} />
                ))}
            </div>
        </div>
    );
};

export default Home;