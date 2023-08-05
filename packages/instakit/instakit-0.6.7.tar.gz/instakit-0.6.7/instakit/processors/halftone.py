#!/usr/bin/env python
# encoding: utf-8
"""
halftone.py

Created by FI$H 2000 on 2012-08-23.
Copyright (c) 2012 Objects In Space And Time, LLC. All rights reserved.
"""
from __future__ import print_function

from abc import ABC, abstractmethod as abstract
from PIL import ImageDraw

from instakit.utils import pipeline, stats
from instakit.utils.gcr import gcr
from instakit.utils.mode import Mode


class ThresholdMatrixProcessor(ABC):
    
    """ Abstract base class for a processor using a uint8 threshold matrix """
    
    LO_TUP = (0,)
    HI_TUP = (255,)
    
    def __init__(self, threshold = 128.0):
        """ Initialize with a threshold value between 0 and 255 """
        self.threshold_matrix = int(threshold)  * self.LO_TUP + \
                           (256-int(threshold)) * self.HI_TUP
    
    @abstract
    def process(self, image): ...


class SlowAtkinson(ThresholdMatrixProcessor):
    
    """ It’s not a joke, this processor is slow as fuck;
        if at all possible, use the cythonized version instead
        (q.v. instakit.processors.ext.Atkinson) and never ever
        use this one if at all possible – unless, like, you’re
        being paid by the hour or somesuch. Up to you dogg.
    """
    
    def process(self, image):
        """ The process call returns a monochrome ('L'-mode) image """
        image = Mode.L.process(image)
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                old = image.getpixel((x, y))
                new = self.threshold_matrix[old]
                err = (old - new) >> 3 # divide by 8.
                image.putpixel((x, y), new)
                for nxy in [(x+1, y),
                            (x+2, y),
                            (x-1, y+1),
                            (x, y+1),
                            (x+1, y+1),
                            (x, y+2)]:
                    try:
                        image.putpixel(nxy, int(
                        image.getpixel(nxy) + err))
                    except IndexError:
                        pass # it happens, evidently.
        return image

class SlowFloydSteinberg(ThresholdMatrixProcessor):
    
    """ A similarly super-slow reference implementation of Floyd-Steinberg.
        Adapted from an RGB version here: https://github.com/trimailov/qwer
    """
    
    # Precalculate fractional error multipliers:
    SEVEN_FRAC = 7/16
    THREE_FRAC = 3/16
    CINCO_FRAC = 5/16
    ALONE_FRAC = 1/16
    
    def process(self, image):
        """ The process call returns a monochrome ('L'-mode) image """
        # N.B. We store local references to the fractional error multipliers
        # to avoid the Python internal-dict-stuff member-lookup overhead:
        image = Mode.L.process(image)
        SEVEN_FRAC = type(self).SEVEN_FRAC
        THREE_FRAC = type(self).THREE_FRAC
        CINCO_FRAC = type(self).CINCO_FRAC
        ALONE_FRAC = type(self).ALONE_FRAC
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                old = image.getpixel((x, y))
                new = self.threshold_matrix[old]
                image.putpixel((x, y), new)
                err = old - new
                for nxy in [((x+1, y),      SEVEN_FRAC),
                            ((x-1, y+1),    THREE_FRAC),
                            ((x, y+1),      CINCO_FRAC),
                            ((x+1, y+1),    ALONE_FRAC)]:
                    try:
                        image.putpixel(nxy[0], int(
                        image.getpixel(nxy[0]) + err * nxy[1]))
                    except IndexError:
                        pass # it happens, evidently.
        return image

class Problematic(object):
    def __init__(self):
        raise TypeError("Fast-math version couldn't be imported")

try:
    # My man, fast Bill Atkinson
    from instakit.processors.ext.halftone import Atkinson as FastAtkinson
except ImportError:
    Atkinson = SlowAtkinson
    FastAtkinson = Problematic
else:
    Atkinson = FastAtkinson

try:
    # THE FLOYDSTER
    from instakit.processors.ext.halftone import FloydSteinberg as FastFloydSteinberg
except ImportError:
    FloydSteinberg = SlowFloydSteinberg
    FastFloydSteinberg = Problematic
else:
    FloydSteinberg = FastFloydSteinberg

class CMYKAtkinson(object):
    
    """ Create a full-color CMYK Atkinson-dithered halftone, with gray-component
        replacement (GCR) at a specified percentage level
    """
    
    def __init__(self, gcr=20):
        self.gcr = max(min(100, gcr), 0)
        self.overprinter = pipeline.ChannelFork(Atkinson, mode='CMYK')
    
    def process(self, image):
        return self.overprinter.process(
            gcr(image, self.gcr))

class CMYKFloydsterBill(object):
    
    """ Create a full-color CMYK Atkinson-dithered halftone, with gray-component
        replacement (GCR) and OH SHIT SON WHAT IS THAT ON THE CYAN CHANNEL DOGG
    """
    
    def __init__(self, gcr=20):
        self.gcr = max(min(100, gcr), 0)
        self.overprinter = pipeline.ChannelFork(Atkinson, mode='CMYK')
        self.overprinter.update({ 'C' : SlowFloydSteinberg() })
    
    def process(self, image):
        return self.overprinter.process(
            gcr(image, self.gcr))

class DotScreen(object):
    
    """ This processor creates a monochrome dot-screen halftone pattern
        from an image. While this may be useful on its own, it is far
        more useful when used across all channels of a CMYK image in
        a ChannelFork or ChannelOverprinter processor operation (q.v.
        `instakit.utils.pipeline.ChannelFork` et al. supra.) serially
        with either a gray-component replacement (GCR) or an under-color
        replacement (UCR) function.
        
        Regarding the latter two operations, instakit only has a basic
        GCR implementation currently, at the time of writing – q.v. the
        `instakit.utils.gcr` module. 
    """
    
    def __init__(self, sample=1, scale=2, angle=0):
        self.sample = sample
        self.scale = scale
        self.angle = angle
    
    def process(self, image):
        orig_width, orig_height = image.size
        image = Mode.L.process(image).rotate(self.angle, expand=1)
        size = image.size[0] * self.scale, image.size[1] * self.scale
        halftone = Mode.L.new(size)
        dotscreen = ImageDraw.Draw(halftone)
        
        for y in range(0, image.size[1], self.sample):
            for x in range(0, image.size[0], self.sample):
                cropbox = image.crop((x,               y,
                                      x + self.sample, y + self.sample))
                diameter = (stats.histogram_mean(cropbox) / 255) ** 0.5
                edge = 0.5 * (1 - diameter)
                xpos, ypos = (x + edge) * self.scale, (y + edge) * self.scale
                boxedge = self.sample * diameter * self.scale
                dotscreen.ellipse((xpos,           ypos,
                                   xpos + boxedge, ypos + boxedge),
                                   fill=255)
        
        halftone = halftone.rotate(-self.angle, expand=1)
        half_width, half_height = halftone.size
        xx = (half_width - orig_width * self.scale) / 2
        yy = (half_height - orig_height * self.scale) / 2
        return halftone.crop((xx, yy, xx + orig_width * self.scale,
                                      yy + orig_height * self.scale))

class CMYKDotScreen(object):
    
    """ Create a full-color CMYK dot-screen halftone, with gray-component
        replacement (GCR), individual rotation angles for each channel’s
        dot-screen, and resampling value controls.
    """
    
    def __init__(self,       gcr=20,
                  sample=10, scale=10,
        thetaC=0, thetaM=15, thetaY=30, thetaK=45):
        
        self.gcr = max(min(100, gcr), 0)
        self.overprinter = pipeline.ChannelFork(DotScreen, mode='CMYK')
        self.overprinter.update({
            'C': DotScreen(angle=thetaC, sample=sample, scale=scale),
            'M': DotScreen(angle=thetaM, sample=sample, scale=scale),
            'Y': DotScreen(angle=thetaY, sample=sample, scale=scale),
            'K': DotScreen(angle=thetaK, sample=sample, scale=scale), })
    
    def process(self, image):
        return self.overprinter.process(
            gcr(image, self.gcr))


if __name__ == '__main__':
    from instakit.utils.static import asset
    
    image_paths = list(map(
        lambda image_file: asset.path('img', image_file),
            asset.listfiles('img')))
    image_inputs = list(map(
        lambda image_path: Mode.RGB.open(image_path),
            image_paths))
    
    for image_input in image_inputs:
        # image_input.show()
        
        Atkinson(threshold=128.0).process(image_input).show()
        # FloydSteinberg(threshold=128.0).process(image_input).show()
        # SlowFloydSteinberg(threshold=128.0).process(image_input).show()
        
        # CMYKAtkinson().process(image_input).show()
        # CMYKFloydsterBill().process(image_input).show()
        # CMYKDotScreen(sample=10, scale=4).process(image_input).show()
    
    print(image_paths)
