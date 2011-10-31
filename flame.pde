int numIter = 100000000;

float xMin = 10*(-0.5);
float xMax = 10*(0.5);
float yMin = 10*(-0.5);
float yMax = 10*(0.5);

float[][][] imgData;
float[][] clrData;
color[] flameColors;

float theta = 0;

void setup()
{
  size(1000, 1000, P2D);
  imgData = new float[width][height][4];
  clrData = new float[width][height];
  flameColors = new color[256];
  createPalette(flameColors);
  loadPixels();
  background(0);
  noLoop();
}

void draw()
{
  float x, y, c;
  float[] p = randomPoint();

  for (int i = 0; i < numIter; i++)
  {
    if (random(1.0) < 0.5)
    {
      c = .5;
      x = 0.164856 * p[0] - 0.775017 * p[1] - 0.400526;
      y = 0.664133 * p[0] + 0.504859 * p[1] + 0.155692;
      p[0] = x;
      p[1] = y;
    }
    else
    {
      c = 0.33;
      x = -0.14321 * p[0] - 0.540632 * p[1] + 2.14451;
      y = 0.427958 * p[0] + 0.0901299 * p[1] + 2.54161;
      p[0] = x;
      p[1] = y;
    }

    applyCamera(p);

    int[] z = pointToImageCoord(p);
    if (z != null && i > 100)
    {
      int m = z[0];
      int n = z[1];
      clrData[m][n] = 0.5 * (clrData[m][n] + c);
      color clr = getColor(clrData[m][n]);
      imgData[m][n][0] += 1;
      imgData[m][n][1] += red(clr);
      imgData[m][n][2] += green(clr);
      imgData[m][n][3] += blue(clr);
    }
  }

  // Apply final transformation

  renderImage(imgData);
  save("flame.png");
}

void renderImage(float[][][] imgData)
{
  float maxFreq = getMaxFreq(imgData);

  for (int i = 0; i < width; i++)
  {
    for (int j = 0; j < height; j++)
    {
      if (imgData[i][j][0] > 0)
      {
        float red = imgData[i][j][1] * (imgData[i][j][0] / maxFreq);
        float green = imgData[i][j][2] * (imgData[i][j][0] / maxFreq);
        float blue = imgData[i][j][3] * (imgData[i][j][0] / maxFreq);
        pixels[i + j * width] = color(red, green, blue);
      }
    }
  }

  updatePixels();
}

void createPalette(color[] flameColors)
{
  color from = color(204, 102, 0);
  color to = color(0, 102, 153);

  for (int i = 0; i < flameColors.length; i++)
  {
    flameColors[i] = lerpColor(from, to, i / 50.0);
  }
}

color getColor(float r)
{
  return flameColors[(int)(r * flameColors.length)];
}

float getMaxFreq(float[][][] imgData)
{
  float max = 0;
  for (int i = 0; i < width; i++)
  {
    for (int j = 0; j < height; j++)
    {
      if (imgData[i][j][0] > max)
      {
        max = imgData[i][j][0];
      }
    }
  }
  return max;
}

void applyCamera(float[] p)
{
  // float zoom = 1.05;
  // p[0] *= zoom;
  // p[1] *= zoom;

  theta += 0.00000001;
  float x, y;
  x = p[0] * cos(theta) - p[1] * sin(theta);
  y = p[0] * sin(theta) + p[1] * cos(theta);
  p[0] = x;
  p[1] = y;
}

float[] randomPoint()
{
  float[] p = new float[2];
  p[0] = random(xMin, xMax);
  p[1] = random(yMin, yMax);
  return p;
}

int[] pointToImageCoord(float[] inPoint)
{
  int[] outPoint = new int[2];
  outPoint[0] = (int)(width * (inPoint[0] - xMin) / (xMax - xMin));
  outPoint[1] = (int)(height * (inPoint[1] - yMin) / (yMax - yMin));

  if (outPoint[0] >= 0 && outPoint[0] < width && outPoint[1] >= 0 && outPoint[1] < height)
  {
    return outPoint;
  }
  else
  {
    return null;
  }
}
