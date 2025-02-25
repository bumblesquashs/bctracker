
class Area {
    constructor(minLat = null, maxLat = null, minLon = null, maxLon = null) {
        this.minLat = minLat === null ? null : parseFloat(minLat);
        this.maxLat = maxLat === null ? null : parseFloat(maxLat);
        this.minLon = minLon === null ? null : parseFloat(minLon);
        this.maxLon = maxLon === null ? null : parseFloat(maxLon);
    }
    
    get isValid() {
        return this.minLat !== null && this.maxLat !== null && this.minLon !== null && this.maxLon !== null;
    }
    
    get isPoint() {
        return this.minLat === this.maxLat && this.minLon === this.maxLon;
    }
    
    get point() {
        return [this.minLon, this.minLat]
    }
    
    get box() {
        return [this.minLon, this.minLat, this.maxLon, this.maxLat]
    }
    
    combine(lat, lon) {
        if (this.minLat === null || lat < this.minLat) {
            this.minLat = lat;
        }
        if (this.maxLat === null || lat > this.maxLat) {
            this.maxLat = lat;
        }
        if (this.minLon === null || lon < this.minLon) {
            this.minLon = lon;
        }
        if (this.maxLon === null || lon > this.maxLon) {
            this.maxLon = lon;
        }
    }
}
