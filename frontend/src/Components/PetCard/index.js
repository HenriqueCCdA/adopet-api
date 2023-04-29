import { Button, CardActionArea, CardActions, CardContent, CardMedia, Typography } from '@mui/material';
import Card from '@mui/material/Card'


function PetCard({pet}) {
  const { id, name, size, age, behavior, photo} = pet

  const petSizes = {
    "S": "Pequeno",
    "M": "Médio",
    "B": "Grande",
  }

  return (
    <Card sx={{maxWidth: 1024}}>
      <CardActionArea>
        <CardMedia
          sx={{ height: 140 }}
          image={photo}
          title={name}
        />
        <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Porte: {petSizes[size]}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Comportamento: {behavior}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Idade: {age}
            </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          Adotar
        </Button>
      </CardActions>
    </Card>
  );
}

export default PetCard;
