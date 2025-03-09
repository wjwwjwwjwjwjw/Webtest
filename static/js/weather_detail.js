/**
 * 天气详情页面的JavaScript
 * 获取和显示详细天气数据
 */

document.addEventListener('DOMContentLoaded', function() {
    // 从URL获取位置参数
    const urlParams = new URLSearchParams(window.location.search);
    const location = urlParams.get('location') || '甘井子区';
    const lat = parseFloat(urlParams.get('lat')) || 38.86;
    const lon = parseFloat(urlParams.get('lon')) || 121.53;
    
    // 更新页面标题
    document.getElementById('detail-location').textContent = location;
    
    // 获取天气数据
    fetchWeatherData(lat, lon, location);
});

/**
 * 获取天气数据
 */
function fetchWeatherData(lat, lon, location) {
    // 在实际应用中，这里应该调用真实的天气API
    // 这里使用模拟数据
    const weatherData = {
        location: location,
        currentWeather: {
            temp: 6,
            feels_like: 8,
            humidity: 65,
            pressure: 1015,
            wind_speed: 12,
            wind_direction: 135, // 0=北, 90=东, 180=南, 270=西
            wind_gust: 23,
            clouds: 0,
            uvi: 3,
            visibility: 4.1,
            aqi: 88,
            description: "晴朗",
            icon: "01d",
            precipitation: 0
        },
        hourlyForecast: [
            { time: "15:00", temp: 8, icon: "01d" },
            { time: "现在", temp: 8, icon: "01d" },
            { time: "16:00", temp: 8, icon: "01d" },
            { time: "17:00", temp: 7, icon: "01d" },
            { time: "17:54", temp: 6, icon: "01d", event: "日落" },
            { time: "18:00", temp: 6, icon: "01n" },
            { time: "19:00", temp: 6, icon: "01n" }
        ],
        dailyForecast: [
            { day: "周一", temp_min: 3, temp_max: 12, icon: "01d" },
            { day: "周二", temp_min: 5, temp_max: 12, icon: "02d" },
            { day: "周三", temp_min: 3, temp_max: 12, icon: "01d" },
            { day: "周四", temp_min: 2, temp_max: 8, icon: "01d" }
        ],
        sunMoon: {
            sunrise: "06:15",
            sunset: "17:53",
            solar_noon: "11小时38分钟",
            moon_phase: 0.5, // 0=新月, 0.25=上弦月, 0.5=满月, 0.75=下弦月
            moon_phase_name: "盈凸月"
        },
        details: {
            temp_desc: "持续降温，将于下午7:00达到最低气温4°。上午3:00达到较高温度3°。",
            feels_like_desc: "主导因素：湿度",
            feels_like_extra: "由于湿度原因，感觉比实际温度更暖和。",
            clouds_desc: "晴朗",
            clouds_extra: "云量将减少，下午4:00时天空无云。今天晚上预计有云。",
            precip_desc: "无降水",
            precip_extra: "未来24小时没有降水。",
            wind_desc: "风力小风，东南风预计将达到风向保持平均速度13公里/小时 (阵风风速为36)。西南风的夜间平均...",
            humidity_desc: "普通",
            humidity_extra: "持续下降，在下午3:48时达到65%的最低值。",
            uv_desc: "中等",
            uv_extra: "今天的最大紫外线辐照量是适中的。",
            aqi_desc: "良",
            aqi_extra: "空气质量良好，主要污染物为: PM2.5 66 μg/m³。",
            visibility_desc: "良好",
            visibility_extra: "在15公里内持续稳定。预计夜晚能见度极好。",
            pressure_trend: "快速下降",
            pressure_time: "15:48 (现在)",
            pressure_extra: "在过去3小时内快速下降。预计在接下来的3小时内将保持上升。"
        }
    };
    
    // 更新UI
    updateWeatherUI(weatherData);
}

/**
 * 更新天气UI
 */
function updateWeatherUI(data) {
    // 更新主要天气信息
    document.getElementById('detail-temperature').textContent = data.currentWeather.temp;
    document.getElementById('detail-weather-desc').textContent = data.currentWeather.description;
    document.getElementById('detail-feels-like').textContent = data.currentWeather.feels_like;
    document.getElementById('detail-humidity').textContent = data.currentWeather.humidity;
    document.getElementById('detail-wind-speed').textContent = data.currentWeather.wind_speed;
    document.getElementById('detail-pressure').textContent = data.currentWeather.pressure;
    document.getElementById('detail-weather-icon').src = `https://openweathermap.org/img/wn/${data.currentWeather.icon}@2x.png`;
    
    // 更新温度卡片
    document.getElementById('grid-temperature').textContent = data.currentWeather.temp;
    document.getElementById('grid-temp-desc').textContent = data.details.temp_desc;
    
    // 更新体感温度卡片
    document.getElementById('grid-feels-like').textContent = data.currentWeather.feels_like;
    document.getElementById('grid-feels-desc').textContent = data.details.feels_like_desc;
    document.getElementById('grid-feels-extra').textContent = data.details.feels_like_extra;
    
    // 更新云量卡片
    document.getElementById('grid-clouds').textContent = data.currentWeather.clouds;
    document.getElementById('grid-clouds-desc').textContent = data.details.clouds_desc;
    document.getElementById('grid-clouds-extra').textContent = data.details.clouds_extra;
    
    // 更新降水卡片
    document.getElementById('grid-precipitation').textContent = data.currentWeather.precipitation;
    document.getElementById('grid-precip-desc').textContent = data.details.precip_desc;
    document.getElementById('grid-precip-extra').textContent = data.details.precip_extra;
    
    // 更新风速卡片
    document.getElementById('grid-wind-speed').textContent = data.currentWeather.wind_speed;
    document.getElementById('grid-wind-gust').textContent = data.currentWeather.wind_gust;
    document.getElementById('grid-wind-desc').textContent = data.details.wind_desc;
    document.getElementById('grid-wind-extra').textContent = "风速";
    
    // 旋转风向指针
    document.getElementById('wind-direction').style.transform = `rotate(${data.currentWeather.wind_direction}deg)`;
    
    // 更新湿度卡片
    document.getElementById('grid-humidity').textContent = data.currentWeather.humidity;
    document.getElementById('grid-humidity-desc').textContent = data.details.humidity_desc;
    document.getElementById('grid-humidity-extra').textContent = data.details.humidity_extra;
    document.getElementById('humidity-bar').style.width = `${data.currentWeather.humidity}%`;
    
    // 更新紫外线卡片
    document.getElementById('grid-uv-index').textContent = data.currentWeather.uvi;
    document.getElementById('grid-uv-desc').textContent = data.details.uv_desc;
    document.getElementById('grid-uv-extra').textContent = data.details.uv_extra;
    document.getElementById('uv-bar').style.width = `${data.currentWeather.uvi / 12 * 100}%`;
    
    // 更新AQI卡片
    document.getElementById('grid-aqi').textContent = data.currentWeather.aqi;
    document.getElementById('grid-aqi-desc').textContent = data.details.aqi_desc;
    document.getElementById('grid-aqi-extra').textContent = data.details.aqi_extra;
    document.getElementById('aqi-bar').style.width = `${data.currentWeather.aqi / 200 * 100}%`;
    
    // 更新可见度卡片
    document.getElementById('grid-visibility').textContent = data.currentWeather.visibility;
    document.getElementById('grid-visibility-desc').textContent = data.details.visibility_desc;
    document.getElementById('grid-visibility-extra').textContent = data.details.visibility_extra;
    document.getElementById('visibility-marker').style.left = `${Math.min(data.currentWeather.visibility / 10 * 100, 100)}%`;
    
    // 更新气压卡片
    document.getElementById('grid-pressure').textContent = data.currentWeather.pressure;
    document.getElementById('grid-pressure-time').textContent = data.details.pressure_time;
    document.getElementById('grid-pressure-trend').textContent = data.details.pressure_trend;
    document.getElementById('grid-pressure-extra').textContent = data.details.pressure_extra;
    
    // 计算气压计的位置 (970-1050hPa)
    const pressurePercent = ((data.currentWeather.pressure - 970) / (1050 - 970)) * 100;
    document.getElementById('pressure-pointer').style.left = `${pressurePercent}%`;
    
    // 更新日出日落卡片
    document.getElementById('sunrise-time').textContent = data.sunMoon.sunrise;
    document.getElementById('sunset-time').textContent = data.sunMoon.sunset;
    document.getElementById('solar-noon').textContent = data.sunMoon.solar_noon;
    
    // 更新月相
    document.getElementById('moon-phase-name').textContent = data.sunMoon.moon_phase_name;
    
    // 计算太阳位置
    const now = new Date();
    const sunrise = new Date();
    const sunset = new Date();
    
    // 解析日出日落时间
    const [sunriseHours, sunriseMinutes] = data.sunMoon.sunrise.split(':').map(Number);
    const [sunsetHours, sunsetMinutes] = data.sunMoon.sunset.split(':').map(Number);
    
    sunrise.setHours(sunriseHours, sunriseMinutes, 0);
    sunset.setHours(sunsetHours, sunsetMinutes, 0);
    
    // 计算太阳位置百分比
    const totalDayTime = sunset - sunrise;
    const currentTimeInDay = now - sunrise;
    
    if (now >= sunrise && now <= sunset) {
        const percentOfDay = Math.min(currentTimeInDay / totalDayTime, 1);
        const sunLeft = percentOfDay * 100;
        const sunTop = Math.sin(Math.PI * percentOfDay) * 100;
        
        document.getElementById('sun-position').style.left = `${sunLeft}%`;
        document.getElementById('sun-position').style.top = `${100 - sunTop}%`;
    } else {
        // 夜间隐藏太阳
        document.getElementById('sun-position').style.opacity = '0';
    }
    
    // 添加动画类
    addAnimations();
}

/**
 * 为元素添加动画
 */
function addAnimations() {
    // 为所有卡片添加交错动画
    const boxes = document.querySelectorAll('.weather-detail-box');
    boxes.forEach((box, index) => {
        setTimeout(() => {
            box.classList.add('animate__animated', 'animate__fadeInUp');
            box.style.animationDelay = `${index * 0.1}s`;
        }, 100);
    });
    
    // 添加温度显示动画
    const tempElement = document.getElementById('detail-temperature');
    tempElement.classList.add('animate__animated', 'animate__fadeIn');
    
    // 风向箭头动画
    const windArrow = document.getElementById('wind-direction');
    windArrow.classList.add('animate__animated', 'animate__bounce');
    setTimeout(() => {
        windArrow.classList.remove('animate__animated', 'animate__bounce');
    }, 1000);
}

/**
 * 格式化日期
 */
function formatDate(date) {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('zh-CN', options);
} 