import React from 'react';
import {
    Home,
    Filter,
    Plus,
    Square,
    CheckCircle,
    AlertTriangle,
    Eye,
    Droplet,
    Sprout,
    Bug,
    Thermometer
} from 'lucide-react';
import '../styles/global.css';

const ActiveCrops = () => {
    return (
        <div className="fade-in">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', marginBottom: '40px' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
                    <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: '8px' }}>
                            <Home size={16} /> / <span style={{ fontWeight: '500' }}>Dashboard</span>
                        </div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: 0, color: 'var(--color-text-dark)' }}>Active Crops</h2>
                        <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>Monitor growth stages and upcoming tasks.</p>
                    </div>
                    <div style={{ display: 'flex', gap: '12px' }}>
                        <button style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '10px 16px',
                            backgroundColor: 'white',
                            border: '1px solid var(--color-border)',
                            borderRadius: '12px',
                            fontWeight: '600',
                            color: 'var(--color-text-dark)'
                        }}>
                            <Filter size={18} /> Filter
                        </button>
                        <button style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '10px 20px',
                            backgroundColor: 'var(--color-primary-green)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '12px',
                            fontWeight: '600',
                            boxShadow: '0 4px 12px rgba(76, 175, 80, 0.3)'
                        }}>
                            <Plus size={18} /> Add New Crop
                        </button>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '32px' }}>

                    {/* Card 1: Wheat */}
                    <CropCard
                        image="https://lh3.googleusercontent.com/aida-public/AB6AXuBoYVt76YGAwzGDCdp05ZWqspBkvj9bB65I7_PbNK6FkL_r5Z9Q8A3zYJOnaRTWAtK4qybhNoLAUuMAuFPiG9aqezeAvojli4gX0gIp2hS1oKj6Mi8re-Ufafqr1uxG7kaE4IOStlak6ofrmflcI90SpB1GQSCBpNUL25WdD9WjdK2Wuh_D07C9G8_eW7EUo_qvAH4hKNL45UQSvM09drK23GtPNaeeGRI-epSr84jBUBMtpYVXd7eHl2DK0FLYkE-v5Jrc7o4MxHw"
                        name="Wheat (Rabi)"
                        acres="5 Acres"
                        status="Healthy"
                        statusColor="green"
                        stageName="Tillering Stage"
                        day="45"
                        totalDays="120"
                        actionIcon={Droplet}
                        actionIconColor="var(--color-accent-ochre)"
                        actionTitle="Next Action"
                        actionDesc="Irrigation required tomorrow morning."
                    />

                    {/* Card 2: Mustard */}
                    <CropCard
                        image="https://lh3.googleusercontent.com/aida-public/AB6AXuDAUqi3mLg4DAMwknkr0iM0SYuQ92brczfaUA1sbXn-Ht2BidsM_VZ3VdfBHHcZMjUpHAmmxrs-JkRmHCbtqJKqH1EyhigfKgpuSazlIH3ROjdXjVkkg5V0UOEvnNxLn3XGrXB2WxStLsF8tZv-pkFs10K8066DcRqingwUB3XxnSmjPZgw9G7GWNqO9R6rdPQ68B3NuQPKJ_DyTPFjYVvIXYGsnXE-9SX7na42ovkr2v2A2o5K8lJ90ekPlYAADEtX3O-RN-rTmVI"
                        name="Mustard"
                        acres="2.5 Acres"
                        status="Needs Attention"
                        statusIcon={AlertTriangle}
                        statusColor="orange"
                        stageName="Flowering Stage"
                        day="65"
                        totalDays="110"
                        actionIcon={Bug}
                        actionIconColor="#D9724C"
                        actionTitle="Next Action"
                        actionDesc="Check for Aphids infestation immediately."
                    />

                    {/* Card 3: Potato */}
                    <CropCard
                        image="https://lh3.googleusercontent.com/aida-public/AB6AXuANYd9vcorDdOrLZPp_Xha2SMKt-DKanRtXBEorOME_NmnQhilnqmNXr6hu_zeyMMyqZ14pARI5F65Kx8JdN7gdbLlhk4vQtaoxITFZNHEPpl9LA9NAW2uMvvxQ_81UHU2FcA8MhvN2KU-QWnyp4_v_WGZoC5q-itS-GDmw9rnTlYDuFHjaBh6Iy8v3Yf_LFzPo1b-GWWQyiRyH6Fbp3PDZWmJVoMuhNG2Ew-SjvKiidsDXM30A6Ao6NL_c1FJk0Qo3dG_hi5GAlfY"
                        name="Potato"
                        acres="1.2 Acres"
                        status="Healthy"
                        statusColor="green"
                        stageName="Vegetative Growth"
                        day="20"
                        totalDays="90"
                        actionIcon={Sprout} // Using Sprout as compost icon substitute
                        actionIconColor="var(--color-primary-green)"
                        actionTitle="Next Action"
                        actionDesc="Apply NPK fertilizer within 3 days."
                    />

                    {/* Card 4: Chickpea */}
                    <CropCard
                        image="https://lh3.googleusercontent.com/aida-public/AB6AXuCcn0uhLmHMd8Bl2F987Hz9d8GBmA7N9Vn6i3tMHmZd-MKH1zuQJmUVyNqFr8F8CQ8c-NlUKBdM2mVCEbOpVErcArmdsx2v7_Rz_fZND8Rx_9NOOJIx412M4yWLf7Py0WzK98S99CuYVawRgspzfSaOCfdYC0p5GZ2ye_8lWkcPdrP774nuXvf89wazlWssf4uQWkO0YEqzszYroWPqAI4dSSweWQ_zukDhWWYNedcwyVYEPQneA4TRAthWQYWOgJJkz-iip0R1pPw"
                        name="Chickpea (Gram)"
                        acres="3.0 Acres"
                        status="Healthy"
                        statusColor="green"
                        stageName="Pod Formation"
                        day="50"
                        totalDays="100"
                        actionIcon={Eye}
                        actionIconColor="var(--color-accent-ochre)"
                        actionTitle="Next Action"
                        actionDesc="Monitor for pod borer activity."
                    />

                    {/* Card 5: Onion */}
                    <CropCard
                        image="https://lh3.googleusercontent.com/aida-public/AB6AXuCjjkkhPkkT63cYZ83eRfboEhYylKaXvH_dYV9H_0Qf7ooXXGQw66N5xaxj8SIZWR2uJe_oPVTknZdxRB1eypHJrA3JzpjPdl5Cl8xISyGOAuNxcI1nayzVx0-jX-7Kf1AmJCwjCbovHL30RxWKzCwwLfOYEp0N8h_ZREI0SG8QojMywV_I5alPuI1_XKl29-nZEqXc963MZ1o2NsUcPso2NZKzrrN6BaW4o5U1yw6UUP9qoYFmuTlDKq9DxrucDq0S2Jw2t2MMlj0"
                        name="Onion"
                        acres="0.8 Acres"
                        status="Thirsty"
                        statusIcon={Droplet} // Using Droplet for water loss/thirsty
                        statusColor="red"
                        stageName="Bulb Development"
                        day="70"
                        totalDays="120"
                        actionIcon={Droplet} // Sprinkler substitute
                        actionIconColor="var(--color-accent-ochre)"
                        actionTitle="Next Action"
                        actionDesc="Light irrigation needed this evening."
                    />

                </div>
            </div>
        </div>
    );
};

const CropCard = ({
    image, name, acres, status, statusColor, statusIcon: StatusIcon = CheckCircle,
    stageName, day, totalDays,
    actionIcon: ActionIcon, actionIconColor, actionTitle, actionDesc
}) => {
    const progress = (parseInt(day) / parseInt(totalDays)) * 100;

    let tagBg, tagText;
    if (statusColor === 'green') { tagBg = '#E8F5E9'; tagText = '#2E7D32'; }
    else if (statusColor === 'orange') { tagBg = '#D96C4C'; tagText = 'white'; } // Needs Attention styled like alert
    else if (statusColor === 'red') { tagBg = '#D96C4C'; tagText = 'white'; }

    // Custom override for specific statuses from design
    const isAlert = status === "Needs Attention" || status === "Thirsty";
    const badgeStyle = isAlert
        ? { backgroundColor: 'rgba(217, 108, 76, 0.9)', color: 'white', backdropFilter: 'blur(4px)' }
        : { backgroundColor: 'rgba(76, 175, 80, 0.9)', color: 'white', backdropFilter: 'blur(4px)' };

    return (
        <div className="card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column', height: '100%' }}>
            {/* Image Header */}
            <div style={{ height: '200px', position: 'relative' }}>
                <img src={image} alt={name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(0,0,0,0.6), transparent)' }}></div>

                <div style={{ position: 'absolute', bottom: '16px', left: '16px', color: 'white' }}>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: 0 }}>{name}</h3>
                    <p style={{ margin: '4px 0 0 0', fontSize: '0.9rem', opacity: 0.9, display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Square size={14} fill="white" /> {acres}
                    </p>
                </div>

                <div style={{
                    position: 'absolute',
                    top: '16px',
                    right: '16px',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    ...badgeStyle
                }}>
                    <StatusIcon size={14} /> {status}
                </div>
            </div>

            {/* Content */}
            <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column' }}>
                <div style={{ marginBottom: '24px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                        <span style={{ color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Growth Stage</span>
                        <span style={{ color: 'var(--color-primary-green)' }}>Day {day} of {totalDays}</span>
                    </div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '8px', color: 'var(--color-text-dark)' }}>{stageName}</div>

                    {/* Progress Bar */}
                    <div style={{ width: '100%', height: '10px', backgroundColor: '#eee', borderRadius: '5px', overflow: 'hidden' }}>
                        <div style={{ width: `${progress}%`, height: '100%', backgroundColor: isAlert ? 'var(--color-accent-ochre)' : 'var(--color-primary-green)' }}></div>
                    </div>
                </div>

                <div style={{
                    backgroundColor: 'white',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid var(--color-border)',
                    marginBottom: '24px',
                    display: 'flex',
                    alignItems: 'start',
                    gap: '12px'
                }}>
                    <div style={{
                        padding: '10px',
                        backgroundColor: `${actionIconColor}20`,
                        borderRadius: '8px',
                        color: actionIconColor
                    }}>
                        <ActionIcon size={20} />
                    </div>
                    <div>
                        <h4 style={{ fontSize: '0.9rem', fontWeight: 'bold', margin: 0 }}>{actionTitle}</h4>
                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: '4px 0 0 0' }}>{actionDesc}</p>
                    </div>
                </div>

                <div style={{ marginTop: 'auto', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                    <button style={{
                        padding: '12px',
                        backgroundColor: 'white',
                        border: '1px solid var(--color-border)',
                        borderRadius: '12px',
                        fontWeight: '600',
                        color: 'var(--color-text-dark)'
                    }}>Details</button>
                    <button style={{
                        padding: '12px',
                        backgroundColor: 'var(--color-primary-green)',
                        borderRadius: '12px',
                        fontWeight: '600',
                        color: 'white',
                        border: 'none'
                    }}>Log Activity</button>
                </div>
            </div>
        </div>
    );
};

export default ActiveCrops;
