# pisoscom
## REIN - Scrapear e indexar los datos de una pagina web

Ejemplo de datos indexados en Elasticsearch:
![image](https://user-images.githubusercontent.com/43989698/203525227-d8af8c6b-f810-4cbc-b998-b04d53d27064.png)

Ejemplo de los datos de un piso indexado:
```json
{
	"_index": "pisoscom",
	"_type": "PISO",
	"_id": "oKS1ioQBX-GuNnSaGtQS",
	"_version": 1,
	"_seq_no": 64,
	"_primary_term": 3,
	"found": true,
	"_source": {
		"url": "https://www.pisos.com/comprar/casa-sant_vicenc_dels_horts_centro_urbano-22591654279_324700/",
		"title": "Casa en calle Laguna",
		"direccion": "Sant Vicenç dels Horts",
		"nHabitaciones": "4 habs.",
		"nBanyos": "3 baños",
		"metrosCuadrados": "393 m²",
		"planta": null,
		"descripcion": "Casa en venta situado en la población de sant vicenç dels horts, provincia de barcelona. \n\nLa vivienda consta de dos plantas, dist...",
		"descuento": "65.200 € (-21%)",
		"imgPreview": "https://fotos.imghs.net/mm//3247/22591654279.324700/3247_22591654279_1_20220304132213263.jpg",
		"precio": "249.000 €",
		"depth": 3,
		"download_timeout": 180,
		"download_slot": "www.pisos.com",
		"download_latency": 0.4934680461883545,
		"superficieConstruida": "393 m²",
		"antiguedad": "Más de 50 años",
		"referencia": "3247-055195",
		"superficieUtil": "350 m²",
		"conservacion": "A reformar",
		"certificado_energetico": "G"
	}
}
```
