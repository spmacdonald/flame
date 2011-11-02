int numIter = 1000000;
int ss = 3;

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
  imgData = new float[ss*width][ss*height][4];
  clrData = new float[ss*width][ss*height];
  flameColors = new color[256];
  createPalette(flameColors);
  loadPixels();
  background(0);
  noLoop();
}

void draw()
{
  float x, y, c;
  float[] p;
  float[] renderPoint;

  p = randomPoint();
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

    renderPoint = p;
    // applyPostTransform(renderPoint);

    int[] z = pointToImageCoord(renderPoint);
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
  float red, green, blue, freq;
  float[][][] smoothedData = new float[width][height][4];

  for (int i = ss; i < ss*width-ss; i++)
  {
    for (int j = ss; j < ss*height-ss; j++)
    {
      red = green = blue = freq = 0;
      for (int k = -ss; k < ss; k++)
      {
        freq += imgData[i+k][j+k][0];
        red += imgData[i+k][j+k][1];
        green += imgData[i+k][j+k][2];
        blue += imgData[i+k][j+k][3];
      }
      smoothedData[i/ss][j/ss][0] = freq / (ss * ss);
      smoothedData[i/ss][j/ss][1] = red / (ss * ss);
      smoothedData[i/ss][j/ss][2] = green / (ss * ss);
      smoothedData[i/ss][j/ss][3] = blue / (ss * ss);
    }
  }

  float maxFreq = getMaxFreq(smoothedData);
  float alpha;

  for (int i = 0; i < width; i++)
  {
    for (int j = 0; j < height; j++)
    {
      if (smoothedData[i][j][0] > 0)
      {
        alpha = pow(log(smoothedData[i][j][0]) / log(maxFreq), 1.0 / 2.2);
        red = alpha * smoothedData[i][j][1] * (smoothedData[i][j][0] / maxFreq);
        green = alpha * smoothedData[i][j][2] * (smoothedData[i][j][0] / maxFreq);
        blue = alpha * smoothedData[i][j][3] * (smoothedData[i][j][0] / maxFreq);
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

void applyPostTransform(float[] p)
{
  float zoom = 1.25;
  p[0] *= zoom;
  p[1] *= zoom;

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
  outPoint[0] = (int)(ss*width * (inPoint[0] - xMin) / (xMax - xMin));
  outPoint[1] = (int)(ss*height * (inPoint[1] - yMin) / (yMax - yMin));

  if (outPoint[0] >= 0 && outPoint[0] < ss*width && outPoint[1] >= 0 && outPoint[1] < ss*height)
  {
    return outPoint;
  }
  else
  {
    return null;
  }
}
