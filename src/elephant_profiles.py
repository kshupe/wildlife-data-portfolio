"""
Individual elephant movement profile generation.
Produces one-page PDF summaries per animal: tracking summary, movement path
map (with Kruger boundary), daily distance time series, and distributions
of step length, speed, and turning angle.

Movement data: Slotow R, Thaker M, Vanak AT (2019) Data from: Fine-scale 
tracking of ambient temperature and movement reveals shuttling behavior of 
elephants to water. Movebank Data Repository. 
https://www.doi.org/10.5441/001/1.403h24q5

Park boundary: UNEP-WCMC and IUCN (2026), Protected Planet: WDPA/WD-OECM 
[Online], July 2026, Cambridge, UK. Available at: www.protectedplanet.net
"""

import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def elephant_profile(df_moves, individual_id):
    """
    Interactive/inline profile for one elephant: prints summary stats and
    displays a folium map, daily distance plot, and distribution histograms
    directly in the notebook. Does not save a file.
    """
    animal = df_moves[df_moves['individual-local-identifier'] == individual_id].copy()
    animal = animal.sort_values('timestamp').reset_index(drop=True)
    animal['date'] = animal['timestamp'].dt.date

    start_date = animal['timestamp'].min()
    end_date = animal['timestamp'].max()
    tracking_days = (end_date - start_date).total_seconds() / 86400

    intervals_hr = animal['step_dt_s'] / 3600
    daily_distance = animal.groupby('date')['step_dist_m'].sum() / 1000
    step_len = animal['step_dist_m'].dropna()
    speed = animal['speed_mps'].dropna()

    print(f"=== Profile: {individual_id} ===")
    print(f"Tracking period: {start_date.date()} to {end_date.date()} ({tracking_days:.1f} days)")
    print(f"Number of fixes: {len(animal)}")
    print(f"Median sampling interval: {intervals_hr.median():.2f} hrs "
          f"(IQR {intervals_hr.quantile(0.25):.2f}-{intervals_hr.quantile(0.75):.2f})")
    print(f"Total distance tracked: {step_len.sum()/1000:.1f} km")
    print(f"Median daily distance: {daily_distance.median():.2f} km")
    print(f"Median step length: {step_len.median():.1f} m "
          f"(IQR {step_len.quantile(0.25):.1f}-{step_len.quantile(0.75):.1f})")
    print(f"Max step length: {step_len.max():.1f} m")
    print(f"Median speed: {speed.median():.3f} m/s "
          f"(IQR {speed.quantile(0.25):.3f}-{speed.quantile(0.75):.3f})")

    import folium
    m = folium.Map(location=[animal['location-lat'].iloc[0], animal['location-long'].iloc[0]], zoom_start=11)
    points = list(zip(animal['location-lat'], animal['location-long']))
    folium.PolyLine(points, color='crimson', weight=2.5, opacity=0.8).add_to(m)
    folium.CircleMarker(points[0], radius=6, color='green', fill=True, popup='Start').add_to(m)
    folium.CircleMarker(points[-1], radius=6, color='black', fill=True, popup='End').add_to(m)

    fig, ax = plt.subplots(figsize=(12, 4))
    daily_distance.plot(ax=ax, marker='o', markersize=3)
    ax.axhline(daily_distance.median(), color='red', linestyle='--',
               label=f"Median: {daily_distance.median():.1f} km")
    ax.set_title(f'{individual_id} - Daily distance')
    ax.set_ylabel('km')
    ax.legend()
    plt.tight_layout()
    plt.show()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    step_len.clip(upper=step_len.quantile(0.99)).hist(bins=40, ax=axes[0])
    axes[0].axvline(step_len.median(), color='red', linestyle='--')
    axes[0].set_title('Step length (m)')
    speed.clip(upper=speed.quantile(0.99)).hist(bins=40, ax=axes[1])
    axes[1].axvline(speed.median(), color='red', linestyle='--')
    axes[1].set_title('Speed (m/s)')
    animal['turn_angle_deg'].dropna().hist(bins=40, ax=axes[2])
    axes[2].set_title('Turning angle (deg)')
    fig.suptitle(f'{individual_id} - Distributions')
    plt.tight_layout()
    plt.show()

    return m


def elephant_profile_pdf(df_moves, individual_id, kruger_boundary, output_dir, preview=True):
    
    """
    Generates a one-page PDF movement profile for one elephant: header,
    static movement-path map (with Kruger boundary overlay), key stats,
    daily distance time series, and step/speed/turning-angle distributions.
    Saves to output_dir and returns the file path.
    """
    animal = df_moves[df_moves['individual-local-identifier'] == individual_id].copy()
    animal = animal.sort_values('timestamp').reset_index(drop=True)
    animal['date'] = animal['timestamp'].dt.date

    start_date = animal['timestamp'].min()
    end_date = animal['timestamp'].max()
    tracking_days = (end_date - start_date).total_seconds() / 86400

    intervals_hr = animal['step_dt_s'] / 3600
    daily_distance = animal.groupby('date')['step_dist_m'].sum() / 1000
    step_len = animal['step_dist_m'].dropna()
    speed = animal['speed_mps'].dropna()
    turn = animal['turn_angle_deg'].dropna()

    fig = plt.figure(figsize=(8.5, 11))
    gs = gridspec.GridSpec(
        nrows=5, ncols=3,
        height_ratios=[0.6, 2.2, 1.3, 1.3, 0.4],
        hspace=0.5, wspace=0.3
    )

    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.75, f"Elephant Movement Profile: {individual_id}",
                  fontsize=18, fontweight='bold', ha='center', va='top')
    ax_title.text(0.5, 0.25,
                  f"Tracked {start_date.date()} to {end_date.date()}  |  "
                  f"{tracking_days:.0f} days  |  {len(animal)} fixes  |  "
                  f"Kruger National Park",
                  fontsize=10, color='dimgray', ha='center', va='top')

    ax_map = fig.add_subplot(gs[1, :2])
    kruger_boundary.boundary.plot(ax=ax_map, color='darkgreen', linewidth=1, alpha=0.6)
    ax_map.plot(animal['location-long'], animal['location-lat'],
                color='saddlebrown', linewidth=0.8, alpha=0.8)
    ax_map.scatter(animal['location-long'].iloc[0], animal['location-lat'].iloc[0],
                   color='green', s=40, zorder=5, label='Start')
    ax_map.scatter(animal['location-long'].iloc[-1], animal['location-lat'].iloc[-1],
                   color='black', s=40, zorder=5, label='End')
    ax_map.set_title('Movement path', fontsize=11, fontweight='bold')
    ax_map.set_xlabel('Longitude', fontsize=8)
    ax_map.set_ylabel('Latitude', fontsize=8)
    ax_map.legend(fontsize=7, loc='upper right')
    ax_map.set_aspect('equal', adjustable='datalim')

    ax_stats = fig.add_subplot(gs[1, 2])
    ax_stats.axis('off')
    stats_text = (
        f"SAMPLING\n"
        f"Median interval: {intervals_hr.median():.1f} hr\n"
        f"IQR: {intervals_hr.quantile(0.25):.1f}-{intervals_hr.quantile(0.75):.1f} hr\n\n"
        f"DISTANCE\n"
        f"Total tracked: {step_len.sum()/1000:.1f} km\n"
        f"Median daily: {daily_distance.median():.2f} km\n\n"
        f"STEP LENGTH\n"
        f"Median: {step_len.median():.0f} m\n"
        f"IQR: {step_len.quantile(0.25):.0f}-{step_len.quantile(0.75):.0f} m\n"
        f"Max: {step_len.max():.0f} m\n\n"
        f"SPEED\n"
        f"Median: {speed.median():.3f} m/s\n"
        f"IQR: {speed.quantile(0.25):.3f}-{speed.quantile(0.75):.3f} m/s"
    )
    ax_stats.text(0.0, 1.0, stats_text, fontsize=9, va='top', ha='left',
                  linespacing=1.6, family='monospace')

    ax_daily = fig.add_subplot(gs[2, :])
    ax_daily.plot(daily_distance.index, daily_distance.values,
                  color='steelblue', linewidth=1)
    ax_daily.axhline(daily_distance.median(), color='crimson', linestyle='--',
                      linewidth=1, label=f"Median: {daily_distance.median():.1f} km")
    ax_daily.set_title('Daily distance traveled', fontsize=11, fontweight='bold')
    ax_daily.set_ylabel('km', fontsize=8)
    ax_daily.tick_params(axis='x', labelsize=7, rotation=45)
    ax_daily.tick_params(axis='y', labelsize=7)
    ax_daily.legend(fontsize=7)

    ax_step = fig.add_subplot(gs[3, 0])
    ax_step.hist(step_len.clip(upper=step_len.quantile(0.99)), bins=30, color='peru')
    ax_step.axvline(step_len.median(), color='crimson', linestyle='--', linewidth=1)
    ax_step.set_title('Step length (m)', fontsize=9, fontweight='bold')
    ax_step.tick_params(labelsize=7)

    ax_speed = fig.add_subplot(gs[3, 1])
    ax_speed.hist(speed.clip(upper=speed.quantile(0.99)), bins=30, color='seagreen')
    ax_speed.axvline(speed.median(), color='crimson', linestyle='--', linewidth=1)
    ax_speed.set_title('Speed (m/s)', fontsize=9, fontweight='bold')
    ax_speed.tick_params(labelsize=7)

    ax_turn = fig.add_subplot(gs[3, 2])
    ax_turn.hist(turn, bins=30, color='slateblue')
    ax_turn.set_title('Turning angle (deg)', fontsize=9, fontweight='bold')
    ax_turn.tick_params(labelsize=7)

    ax_footer = fig.add_subplot(gs[4, :])
    ax_footer.axis('off')
    ax_footer.text(0.5, 0.9,
                    "Distances are straight-line displacements between consecutive fixes; "
                    "medians and IQR used due to right-skewed movement data.",
                    fontsize=6, style='italic', color='gray', ha='center', va='top')
    ax_footer.text(0.5, 0.45,
                    "Movement data: Slotow R, Thaker M, Vanak AT (2019) Data from: Fine-scale "
                    "tracking of ambient temperature and movement reveals shuttling behavior of "
                    "elephants to water. Movebank Data Repository. "
                    "https://www.doi.org/10.5441/001/1.403h24q5",
                    fontsize=6, style='italic', color='gray', ha='center', va='top')
    ax_footer.text(0.5, 0.0,
                    "Park boundary: UNEP-WCMC and IUCN (2026), Protected Planet: WDPA/WD-OECM "
                    "[Online], July 2026, Cambridge, UK. Available at: www.protectedplanet.net",
                    fontsize=6, style='italic', color='gray', ha='center', va='top')

    os.makedirs(output_dir, exist_ok=True)
    safe_id = str(individual_id).replace(" ", "_").replace("/", "-")
    filepath = os.path.join(output_dir, f"{safe_id}_profile.pdf")
    fig.savefig(filepath, format='pdf', bbox_inches='tight', dpi=300)

    if preview:
        plt.show()
    else:
        plt.close(fig)

    print(f"Saved: {filepath}")
    return filepath
