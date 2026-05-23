(function(){
  var form = document.getElementById('mc-form');
  if(!form) return;
  var out = document.getElementById('mc-result');

  // Volume estimates (cubic feet) per property size + adjustment for services
  var BASE_VOLUME = {
    'studio': 220, '1bed': 350, '2bed': 600, '3bed': 950, '4bed': 1400, '5bed': 1900,
    'office-small': 400, 'office-medium': 900, 'office-large': 1700
  };

  // Van sizes
  function vanFor(cubic){
    if(cubic <= 250) return {name:'Small Luton (~250 cu ft)', count:1};
    if(cubic <= 600) return {name:'Standard Luton (~600 cu ft)', count:1};
    if(cubic <= 1200) return {name:'Large Luton (~1,200 cu ft)', count:1};
    if(cubic <= 1800) return {name:'7.5-tonne lorry (~1,800 cu ft)', count:1};
    if(cubic <= 3600) return {name:'7.5-tonne lorry (~1,800 cu ft)', count:2};
    return {name:'18-tonne lorry (~3,200 cu ft)', count: Math.ceil(cubic/3200)};
  }

  // Base price bands (2026 indicative — refined at survey)
  function priceFor(size, distance, packing, storageWeeks){
    var base = {
      'studio': 425, '1bed': 575, '2bed': 700, '3bed': 925, '4bed': 1300, '5bed': 1800,
      'office-small': 850, 'office-medium': 1650, 'office-large': 2900
    }[size] || 700;
    // distance: short (<10) / medium (10-50) / long (50-200) / national (>200)
    var distMul = distance === 'short' ? 1.0 : distance === 'medium' ? 1.15 : distance === 'long' ? 1.4 : 1.85;
    var withDist = Math.round(base * distMul);
    // packing
    var pack = packing === 'full' ? Math.round(withDist * 0.35) : packing === 'fragile' ? Math.round(withDist * 0.15) : 0;
    // storage per week
    var storage = (storageWeeks > 0) ? storageWeeks * 60 : 0;
    return {
      base: withDist,
      packing: pack,
      storage: storage,
      total: withDist + pack + storage,
    };
  }

  function fmt(n){
    return '£' + n.toLocaleString('en-GB');
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var size = form.elements['size'].value;
    var distance = form.elements['distance'].value;
    var packing = form.elements['packing'].value;
    var storage = parseInt(form.elements['storage'].value || '0', 10);
    if(!size || !distance){
      out.innerHTML = '<p style="color:var(--orange-dark);font-weight:700">Please choose property size and distance.</p>';
      return;
    }
    var cubic = BASE_VOLUME[size] || 600;
    var van = vanFor(cubic);
    var price = priceFor(size, distance, packing, storage);
    var rangeLo = Math.round(price.total * 0.9);
    var rangeHi = Math.round(price.total * 1.15);

    out.innerHTML =
      '<div style="background:var(--cream);border:2px solid var(--orange);border-radius:14px;padding:1.4rem 1.4rem 1.2rem;margin-top:1.5rem">' +
        '<div style="display:flex;align-items:baseline;gap:.6rem;flex-wrap:wrap">' +
          '<h3 style="margin:0;color:var(--navy)">Indicative price band</h3>' +
          '<span style="color:var(--muted);font-size:13.5px">Refined at survey · valid 60 days</span>' +
        '</div>' +
        '<div style="font-size:clamp(2rem,3.5vw,2.6rem);font-family:var(--font-display);font-weight:800;color:var(--orange-dark);margin:.4rem 0 .25rem">' + fmt(rangeLo) + ' – ' + fmt(rangeHi) + '</div>' +
        '<div style="color:var(--muted);font-size:14px;margin-bottom:.85rem">Includes labour, vehicle, fuel, insurance and parking permits. Excludes optional add-ons not selected above.</div>' +
        '<table style="width:100%;border-collapse:collapse;font-size:14.5px">' +
          '<tr><td style="padding:.4rem 0;color:var(--muted)">Estimated volume</td><td style="padding:.4rem 0;text-align:right;font-weight:700">' + cubic + ' cubic ft</td></tr>' +
          '<tr><td style="padding:.4rem 0;color:var(--muted)">Recommended vehicle</td><td style="padding:.4rem 0;text-align:right;font-weight:700">' + (van.count > 1 ? van.count + '× ' : '') + van.name + '</td></tr>' +
          '<tr><td style="padding:.4rem 0;color:var(--muted)">Base move</td><td style="padding:.4rem 0;text-align:right;font-weight:700">' + fmt(price.base) + '</td></tr>' +
          (price.packing ? '<tr><td style="padding:.4rem 0;color:var(--muted)">Packing service</td><td style="padding:.4rem 0;text-align:right;font-weight:700">' + fmt(price.packing) + '</td></tr>' : '') +
          (price.storage ? '<tr><td style="padding:.4rem 0;color:var(--muted)">Storage (' + storage + ' wk)</td><td style="padding:.4rem 0;text-align:right;font-weight:700">' + fmt(price.storage) + '</td></tr>' : '') +
        '</table>' +
        '<div style="margin-top:1rem;display:flex;flex-wrap:wrap;gap:.65rem"><a href="../quote.html" class="btn">Get an exact written quote</a><a href="tel:+441782939124" class="btn btn-ghost">Call 01782 939124</a></div>' +
        '<p style="color:var(--muted);font-size:12.5px;margin:1rem 0 0">This estimate is indicative only. Your fixed-price written quote is confirmed after a free home or video survey and is valid 60 days. Storage from £40/wk per palletised unit; ' +
        'packing prices indicative — refined at survey based on your specific items and access.</p>' +
      '</div>';
    out.scrollIntoView({behavior:'smooth', block:'start'});
  });
})();
