import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.css";
import { Link } from "react-router-dom";

export const Home = () => {
    const { store, actions } = useContext(Context);
    const [OpenIndex, setOpenIndex] = useState(null);

    const frequentQuestionsList = [
        { question: "¿Qué es Lorem ipsum?", answer: "Lorem ipsum es un texto de relleno utilizado en diseño gráfico y tipografía." },
        { question: "¿Por qué usar Lorem ipsum?", answer: "Se usa como relleno para mostrar el diseño y no el contenido final." },
        { question: "¿Cuántos caracteres tiene Lorem ipsum?", answer: "Originalmente tiene 5,400 caracteres aproximadamente." },
        { question: "¿Es Lorem ipsum legible?", answer: "No, es un texto sin sentido legible y sin significado real." },
        { question: "¿Quién creo Lorem ipsum?", answer: "El texto tiene sus orígenes en el año 1500 por un autor desconocido." },
        { question: "¿Cuándo se popularizó Lorem ipsum?", answer: "En el siglo XX, con la publicación de Letraset." },
        { question: "¿Dónde puedo encontrar Lorem ipsum?", answer: "Se puede encontrar fácilmente en internet en varios idiomas." }
    ];

    const handleItemClick = (index) => {
        if (OpenIndex === index) {
            setOpenIndex(null);
        } else {
            setOpenIndex(index);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-md-6">
                    <h1>Crea tu agenda inteligente gratuita</h1>
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Donec et mi dictum, ultricies metus vel, imperdiet turpis. Sed in odio mattis, 
                        consectetur lacus auctor, egestas tortor. Vestibulum augue tortor, rutrum eu lectus ut, viverra pretium ligula. 
                        Proin vitae elit aliquet, pretium metus quis, aliquet urna. Curabitur elementum ex vitae nulla molestie, non varius nibh congue. 
                        Praesent cursus lacus sit amet quam egestas placerat. Pellentesque vel ullamcorper ante, 
                        sed elementum enim. Proin eleifend non urna sit amet congue. 
                        Quisque sollicitudin mattis nisl, at iaculis nisi sodales quis. Maecenas vel facilisis augue.
                    </p>
                </div>
                <div className="col-md-6">
                    <img src="https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg" className="img-fluid" />
                </div>
            </div>
            <div className="row mt-5">
                <div className="col-md-6">
                    <img src="https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg" className="img-fluid" />
                </div>
                <div className="col-md-6">
                    <h1>Title</h1>
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Donec et mi dictum, ultricies metus vel, imperdiet turpis. Sed in odio mattis, 
                        consectetur lacus auctor, egestas tortor. Vestibulum augue tortor, rutrum eu lectus ut, viverra pretium ligula. 
                        Proin vitae elit aliquet, pretium metus quis, aliquet urna. Curabitur elementum ex vitae nulla molestie, non varius nibh congue. 
                        Praesent cursus lacus sit amet quam egestas placerat. Pellentesque vel ullamcorper ante, 
                        sed elementum enim. Proin eleifend non urna sit amet congue. 
                        Quisque sollicitudin mattis nisl, at iaculis nisi sodales quis. Maecenas vel facilisis augue.
                    </p>
                </div>
            </div>
            <div className="row mt-5">
                <div className="col-md-3">
                    <div className="card">
                        <img src="https://via.placeholder.com/150" className="card-img-top" alt="Imagen 1" />
                        <div className="card-body">
                            <h5 className="card-title">Título de la Carta 1</h5>
                            <p className="card-text">Descripción breve de la carta 1.</p>
                            <a href="#" className="btn btn-primary">Ver más</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card">
                        <img src="https://via.placeholder.com/150" className="card-img-top" alt="Imagen 2" />
                        <div className="card-body">
                            <h5 className="card-title">Título de la Carta 2</h5>
                            <p className="card-text">Descripción breve de la carta 2.</p>
                            <a href="#" className="btn btn-primary">Ver más</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card">
                        <img src="https://via.placeholder.com/150" className="card-img-top" alt="Imagen 3" />
                        <div className="card-body">
                            <h5 className="card-title">Título de la Carta 3</h5>
                            <p className="card-text">Descripción breve de la carta 3.</p>
                            <a href="#" className="btn btn-primary">Ver más</a>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card">
                        <img src="https://via.placeholder.com/150" className="card-img-top" alt="Imagen 4" />
                        <div className="card-body">
                            <h5 className="card-title">Título de la Carta 4</h5>
                            <p className="card-text">Descripción breve de la carta 4.</p>
                            <a href="#" className="btn btn-primary">Ver más</a>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row mt-5">
                <div className="col-md-6">
                    <h1>Title</h1>
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                        Donec et mi dictum, ultricies metus vel, imperdiet turpis. Sed in odio mattis, 
                        consectetur lacus auctor, egestas tortor. Vestibulum augue tortor, rutrum eu lectus ut, viverra pretium ligula. 
                        Proin vitae elit aliquet, pretium metus quis, aliquet urna. Curabitur elementum ex vitae nulla molestie, non varius nibh congue. 
                        Praesent cursus lacus sit amet quam egestas placerat. Pellentesque vel ullamcorper ante, 
                        sed elementum enim. Proin eleifend non urna sit amet congue. 
                        Quisque sollicitudin mattis nisl, at iaculis nisi sodales quis. Maecenas vel facilisis augue.
                    </p>
                </div>
                <div className="col-md-6">
                    <img src="https://static.vecteezy.com/system/resources/previews/004/141/669/non_2x/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg" className="img-fluid" />
                </div>
            </div>
            <div className="row mt-5">
                <div className="col-md-12">
                    <div className="extra-information">
                        <h1>Title</h1>
                        <p>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                            Donec et mi dictum, ultricies metus vel, imperdiet turpis. Sed in odio mattis, 
                            consectetur lacus auctor, egestas tortor. Vestibulum augue tortor, rutrum eu lectus ut, viverra pretium ligula. 
                            Proin vitae elit aliquet, pretium metus quis, aliquet urna. Curabitur elementum ex vitae nulla molestie, non varius nibh congue. 
                            Praesent cursus lacus sit amet quam egestas placerat. Pellentesque vel ullamcorper ante, 
                            sed elementum enim. Proin eleifend non urna sit amet congue. 
                            Quisque sollicitudin mattis nisl, at iaculis nisi sodales quis. Maecenas vel facilisis augue.
                        </p>
                    </div>
                </div>
            </div>
            <div className="row mt-5">
                <div className="col-md-12">
                    <div className="bottom">
                        <h1>Preguntas frecuentes</h1>
                        {frequentQuestionsList.map((item, index) => (
                            <div key={index} className="fq-item">
                                <div
                                    className={`fq-question ${OpenIndex === index ? 'active' : ''}`}
                                    onClick={() => handleItemClick(index)}
                                >
                                    {item.question}
                                </div>
                                {OpenIndex === index && (
                                    <div className="fq-answer">
                                        <p>{item.answer}</p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};
